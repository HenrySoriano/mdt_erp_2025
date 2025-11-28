"""
Vistas para modo offline
"""
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import json


@login_required
def offline_page(request):
    """Página mostrada cuando no hay conexión"""
    return render(request, 'offline.html')


@require_http_methods(["GET"])
def manifest_view(request):
    """Servir el manifest.json"""
    from django.conf import settings
    import os
    
    manifest_path = os.path.join(settings.BASE_DIR, 'theme', 'static', 'manifest.json')
    
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest_data = json.load(f)
        return JsonResponse(manifest_data, safe=False)
    except FileNotFoundError:
        return JsonResponse({'error': 'Manifest not found'}, status=404)


@require_http_methods(["GET"])
def service_worker_view(request):
    """Servir el service-worker.js"""
    from django.conf import settings
    import os
    
    sw_path = os.path.join(settings.BASE_DIR, 'theme', 'static', 'js', 'service-worker.js')
    
    try:
        with open(sw_path, 'r', encoding='utf-8') as f:
            content = f.read()
        response = HttpResponse(content, content_type='application/javascript')
        response['Service-Worker-Allowed'] = '/'
        return response
    except FileNotFoundError:
        return HttpResponse('// Service Worker not found', content_type='application/javascript')

