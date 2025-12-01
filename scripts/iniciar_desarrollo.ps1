# Script PowerShell para iniciar el servidor Django con MySQL
# Este script configura todo automáticamente para desarrollo

Write-Host "=== INICIANDO SERVIDOR DJANGO CON MySQL ===" -ForegroundColor Green
Write-Host ""

# Verificar que XAMPP esté corriendo
Write-Host "Verificando MySQL (XAMPP)..." -ForegroundColor Yellow
try {
    $mysqlProcess = Get-Process -Name "mysqld" -ErrorAction SilentlyContinue
    if ($mysqlProcess) {
        Write-Host "✅ MySQL está corriendo" -ForegroundColor Green
    } else {
        Write-Host "⚠️  MySQL no está corriendo" -ForegroundColor Yellow
        Write-Host "   Por favor, inicia MySQL desde XAMPP Control Panel" -ForegroundColor Yellow
        Write-Host ""
        $continuar = Read-Host "¿Deseas continuar de todas formas? (s/n)"
        if ($continuar -ne "s") {
            exit
        }
    }
} catch {
    Write-Host "⚠️  No se pudo verificar MySQL" -ForegroundColor Yellow
}

# Configurar variables de entorno para MySQL
Write-Host ""
Write-Host "Configurando variables de entorno..." -ForegroundColor Yellow
$env:USE_MYSQL_LOCAL = "True"
$env:DB_NAME = "mdt_erp_dev"
$env:DB_USER = "root"
$env:DB_PASSWORD = ""
$env:DB_HOST = "127.0.0.1"
$env:DB_PORT = "3306"

Write-Host "✅ Variables configuradas:" -ForegroundColor Green
Write-Host "   USE_MYSQL_LOCAL = $env:USE_MYSQL_LOCAL"
Write-Host "   DB_NAME = $env:DB_NAME"
Write-Host "   DB_USER = $env:DB_USER"
Write-Host "   DB_HOST = $env:DB_HOST"
Write-Host "   DB_PORT = $env:DB_PORT"
Write-Host ""

# Verificar conexión a la base de datos
Write-Host "Verificando conexión a MySQL..." -ForegroundColor Yellow
try {
    $checkResult = & .\venv\Scripts\python.exe manage.py check --database default 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Conexión a MySQL exitosa" -ForegroundColor Green
    } else {
        Write-Host "❌ Error al conectar a MySQL:" -ForegroundColor Red
        Write-Host $checkResult
        Write-Host ""
        Write-Host "Verifica que:" -ForegroundColor Yellow
        Write-Host "  1. MySQL esté corriendo en XAMPP"
        Write-Host "  2. La base de datos 'mdt_erp_dev' exista"
        Write-Host "  3. Las credenciales sean correctas"
        exit 1
    }
} catch {
    Write-Host "❌ Error al verificar conexión: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== INICIANDO SERVIDOR ===" -ForegroundColor Green
Write-Host "Servidor disponible en: http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "Presiona Ctrl+C para detener" -ForegroundColor Yellow
Write-Host ""

# Iniciar servidor
& .\venv\Scripts\python.exe manage.py runserver

