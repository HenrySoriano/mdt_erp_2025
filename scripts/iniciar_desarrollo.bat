@echo off
REM Script batch para iniciar el servidor Django con MySQL en Windows
REM Este script configura todo automáticamente para desarrollo

echo === INICIANDO SERVIDOR DJANGO CON MySQL ===
echo.

REM Configurar variables de entorno para MySQL
set USE_MYSQL_LOCAL=True
set DB_NAME=mdt_erp_dev
set DB_USER=root
set DB_PASSWORD=
set DB_HOST=127.0.0.1
set DB_PORT=3306

echo Variables configuradas:
echo   USE_MYSQL_LOCAL=%USE_MYSQL_LOCAL%
echo   DB_NAME=%DB_NAME%
echo   DB_USER=%DB_USER%
echo   DB_HOST=%DB_HOST%
echo   DB_PORT=%DB_PORT%
echo.

echo === INICIANDO SERVIDOR ===
echo Servidor disponible en: http://127.0.0.1:8000
echo Presiona Ctrl+C para detener
echo.

REM Iniciar servidor
venv\Scripts\python.exe manage.py runserver

pause

