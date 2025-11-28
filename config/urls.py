"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from apps.presentation.views import auth_views, admin_views, employee_views, offline_views

urlpatterns = [
    path('django-admin/', admin.site.urls),
    
    # Authentication
    path('', auth_views.login_view, name='login'),
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    
    # Admin URLs
    path('admin/dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('superuser/dashboard/', admin_views.superuser_dashboard, name='superuser_dashboard'),
    path('admin/companies/', admin_views.company_list, name='company_list'),
    path('admin/companies/create/', admin_views.create_company, name='create_company'),
    path('admin/companies/<int:company_id>/edit/', admin_views.edit_company, name='edit_company'),
    path('admin/companies/<int:company_id>/progress/', admin_views.company_progress, name='company_progress'),
    path('admin/employees/', admin_views.employee_list, name='employee_list'),
    path('admin/employees/create/', admin_views.create_employee, name='create_employee'),
    path('admin/employees/<int:employee_id>/', admin_views.employee_detail, name='employee_detail'),
    path('admin/employees/<int:employee_id>/edit/', admin_views.edit_employee, name='edit_employee'),
    path('admin/employees/<int:employee_id>/toggle-status/', admin_views.employee_toggle_status, name='employee_toggle_status'),
    path('admin/employees/<int:employee_id>/delete/', admin_views.employee_delete, name='employee_delete'),
    path('admin/employees/bulk-delete/', admin_views.employee_bulk_delete, name='employee_bulk_delete'),
    path('admin/employees/export/', admin_views.employee_export, name='employee_export'),
    path('admin/employees/company/<int:company_id>/', admin_views.employee_list, name='employee_list_by_company'),
    path('admin/employees/company/<int:company_id>/export/', admin_views.employee_export, name='employee_export_by_company'),
    path('admin/results/', admin_views.evaluation_results, name='evaluation_results'),
    path('admin/results/company/<int:company_id>/', admin_views.evaluation_results, name='evaluation_results_by_company'),
    path('admin/results/pdf/', admin_views.download_admin_results_pdf, name='download_admin_results_pdf'),
    path('admin/results/company/<int:company_id>/pdf/', admin_views.download_admin_results_pdf, name='download_admin_results_pdf_by_company'),
    
    # PowerPoint con Playwright (nuevas rutas)
    path('admin/results/preview-pptx/', admin_views.preview_pptx_report, name='preview_pptx_report'),
    path('admin/results/company/<int:company_id>/preview-pptx/', admin_views.preview_pptx_report, name='preview_pptx_report_by_company'),
    path('admin/results/pptx-progress/', admin_views.pptx_progress_page, name='pptx_progress'),
    path('admin/results/company/<int:company_id>/pptx-progress/', admin_views.pptx_progress_page, name='pptx_progress_by_company'),
    path('admin/results/generate-pptx/', admin_views.generate_pptx_with_screenshots, name='generate_pptx_with_screenshots'),
    path('admin/results/company/<int:company_id>/generate-pptx/', admin_views.generate_pptx_with_screenshots, name='generate_pptx_with_screenshots_by_company'),
    
    # PDF con Playwright (nuevas rutas)
    path('admin/results/preview-pdf/', admin_views.pdf_preview_page, name='pdf_preview'),
    path('admin/results/company/<int:company_id>/preview-pdf/', admin_views.pdf_preview_page, name='pdf_preview_by_company'),
    path('admin/results/pdf-progress/', admin_views.pdf_progress_page, name='pdf_progress'),
    path('admin/results/company/<int:company_id>/pdf-progress/', admin_views.pdf_progress_page, name='pdf_progress_by_company'),
    path('admin/results/generate-pdf-playwright/', admin_views.generate_pdf_with_playwright, name='generate_pdf_playwright'),
    path('admin/results/company/<int:company_id>/generate-pdf-playwright/', admin_views.generate_pdf_with_playwright, name='generate_pdf_playwright_by_company'),
    
    path('admin/results/excel-anonymous/', admin_views.download_anonymous_evaluations_excel, name='download_anonymous_evaluations_excel'),
    path('admin/results/company/<int:company_id>/excel-anonymous/', admin_views.download_anonymous_evaluations_excel, name='download_anonymous_evaluations_excel_by_company'),
    path('admin/evaluation/<int:evaluation_id>/view/', admin_views.admin_view_evaluation, name='admin_view_evaluation'),
    path('admin/evaluation/preview/', admin_views.admin_view_empty_evaluation, name='admin_view_empty_evaluation'),
    path('admin/bulk-import/', admin_views.bulk_import, name='bulk_import'),
    path('admin/download-template/', admin_views.download_import_template, name='download_import_template'),
    
    # Employee URLs
    path('employee/dashboard/', employee_views.employee_dashboard, name='employee_dashboard'),
    path('employee/evaluation/start/', employee_views.start_evaluation, name='start_evaluation'),
    path('employee/evaluation/<int:evaluation_id>/', employee_views.take_evaluation, name='take_evaluation'),
    path('employee/evaluation/<int:evaluation_id>/results/', employee_views.view_evaluation_results, name='view_evaluation_results'),
    path('employee/evaluation/<int:evaluation_id>/results/pdf/', employee_views.download_evaluation_pdf, name='download_evaluation_pdf'),
    path('employee/compare/', employee_views.compare_evaluations, name='compare_evaluations'),
    
    # Django Browser Reload
    path("__reload__/", include("django_browser_reload.urls")),
    
    # PWA Routes
    path('manifest.json', offline_views.manifest_view, name='manifest'),
    path('service-worker.js', offline_views.service_worker_view, name='service_worker'),
    path('offline/', offline_views.offline_page, name='offline_page'),
]
