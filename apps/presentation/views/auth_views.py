from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.infrastructure.models import CustomUser


def login_view(request):
    """Vista para el login de usuarios"""
    if request.user.is_authenticated:
        return _redirect_by_role(request.user)
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Django's authenticate expects 'username' parameter even if USERNAME_FIELD is 'email'
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenido {user.email}')
            return _redirect_by_role(user)
        else:
            messages.error(request, 'Email o contraseña incorrectos')
    
    return render(request, 'auth/login.html')


def _redirect_by_role(user):
    """Redirige al usuario según su rol"""
    if user.is_superuser or user.role == CustomUser.Role.SUPERUSER:
        return redirect('superuser_dashboard')
    elif user.role == CustomUser.Role.COMPANY_ADMIN:
        return redirect('admin_dashboard')
    elif user.role == CustomUser.Role.EMPLOYEE:
        return redirect('employee_dashboard')
    else:
        return redirect('login')


@login_required
def logout_view(request):
    """Vista para cerrar sesión"""
    logout(request)
    messages.info(request, 'Sesión cerrada exitosamente')
    return redirect('login')
