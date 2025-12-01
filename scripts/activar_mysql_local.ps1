# Script PowerShell para activar MySQL local con XAMPP
# Ejecuta este script antes de usar manage.py cuando quieras usar MySQL

Write-Host "=== ACTIVANDO MySQL LOCAL (XAMPP) ===" -ForegroundColor Green
Write-Host ""

# Configurar variables de entorno para esta sesión
$env:USE_MYSQL_LOCAL = "True"
$env:DB_NAME = "mdt_erp_dev"
$env:DB_USER = "root"
$env:DB_PASSWORD = ""
$env:DB_HOST = "127.0.0.1"
$env:DB_PORT = "3306"

Write-Host "✅ Variables de entorno configuradas:" -ForegroundColor Green
Write-Host "   USE_MYSQL_LOCAL = $env:USE_MYSQL_LOCAL"
Write-Host "   DB_NAME = $env:DB_NAME"
Write-Host "   DB_USER = $env:DB_USER"
Write-Host "   DB_HOST = $env:DB_HOST"
Write-Host "   DB_PORT = $env:DB_PORT"
Write-Host ""
Write-Host "⚠️  IMPORTANTE: Estas variables solo están activas en esta sesión de PowerShell" -ForegroundColor Yellow
Write-Host "   Para usar MySQL, ejecuta los comandos Django en esta misma ventana" -ForegroundColor Yellow
Write-Host ""
Write-Host "Ejemplos de comandos:" -ForegroundColor Cyan
Write-Host "   .\venv\Scripts\python.exe manage.py migrate"
Write-Host "   .\venv\Scripts\python.exe manage.py runserver"
Write-Host "   .\venv\Scripts\python.exe manage.py createsuperuser"
Write-Host ""

