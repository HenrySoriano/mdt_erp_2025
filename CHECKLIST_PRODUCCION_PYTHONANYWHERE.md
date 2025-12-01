# ✅ Checklist de Producción para PythonAnywhere

## 🔒 1. SEGURIDAD

### Variables de Entorno
- [ ] **SECRET_KEY**: Configurada en variables de entorno de PythonAnywhere
  ```bash
  export DJANGO_SECRET_KEY='tu-secret-key-super-segura-aqui'
  ```
- [ ] **DEBUG**: Desactivado (`DEBUG=False`)
- [ ] **ALLOWED_HOSTS**: Configurado con tu dominio de PythonAnywhere
- [ ] **CSRF_TRUSTED_ORIGINS**: Incluye `https://tuusuario.pythonanywhere.com`
- [ ] **Base de Datos**: Credenciales en variables de entorno
  ```bash
  export DB_NAME='tuusuario$default'
  export DB_USER='tuusuario'
  export DB_PASSWORD='tu-password-mysql'
  export DB_HOST='tuusuario.mysql.pythonanywhere-services.com'
  export DB_PORT='3306'
  ```

### Configuración de Seguridad
- [ ] `SECURE_SSL_REDIRECT = True`
- [ ] `SESSION_COOKIE_SECURE = True`
- [ ] `CSRF_COOKIE_SECURE = True`
- [ ] `SECURE_HSTS_SECONDS` configurado
- [ ] `X_FRAME_OPTIONS = 'DENY'`
- [ ] Contraseñas encriptadas (ya implementado con `cryptography`)

### Archivos Sensibles
- [ ] `.env` está en `.gitignore` ✅
- [ ] `db.sqlite3` está en `.gitignore` ✅
- [ ] `__pycache__/` está en `.gitignore` ✅
- [ ] `venv/` está en `.gitignore` ✅
- [ ] No hay secretos hardcodeados en el código ✅

## 📦 2. CONFIGURACIÓN DE PYTHONANYWHERE

### Base de Datos MySQL
- [ ] Base de datos MySQL creada en PythonAnywhere
- [ ] Credenciales configuradas en variables de entorno
- [ ] Migraciones ejecutadas: `python3.10 manage.py migrate`
- [ ] Superusuario creado: `python3.10 manage.py createsuperuser`

### Archivos Estáticos
- [ ] `STATIC_ROOT` configurado: `/home/tuusuario/mdt_erp_2025/staticfiles`
- [ ] `collectstatic` ejecutado: `python3.10 manage.py collectstatic --noinput`
- [ ] Ruta estática configurada en Web App:
  - URL: `/static/`
  - Directory: `/home/tuusuario/mdt_erp_2025/staticfiles`

### Archivos Media (si aplica)
- [ ] `MEDIA_ROOT` configurado: `/home/tuusuario/mdt_erp_2025/media`
- [ ] Ruta media configurada en Web App:
  - URL: `/media/`
  - Directory: `/home/tuusuario/mdt_erp_2025/media`

### WSGI Configuration
- [ ] Archivo WSGI configurado correctamente:
  ```python
  import os
  import sys
  
  path = '/home/tuusuario/mdt_erp_2025'
  if path not in sys.path:
      sys.path.append(path)
  
  os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
  
  from django.core.wsgi import get_wsgi_application
  application = get_wsgi_application()
  ```

## 🗄️ 3. BASE DE DATOS

### Migraciones
- [ ] Todas las migraciones aplicadas: `python3.10 manage.py migrate`
- [ ] No hay migraciones pendientes: `python3.10 manage.py showmigrations`
- [ ] Datos iniciales cargados (si aplica):
  ```bash
  python3.10 manage.py loaddata apps/infrastructure/fixtures/dimensions.json
  python3.10 manage.py loaddata apps/infrastructure/fixtures/questions.json
  ```

### Backup
- [ ] Script de backup configurado (opcional pero recomendado)
- [ ] Proceso de backup automatizado (si aplica)

## 📋 4. DEPENDENCIAS

### Instalación
- [ ] Python 3.10 seleccionado en PythonAnywhere
- [ ] Todas las dependencias instaladas:
  ```bash
  pip3.10 install --user -r requirements.txt
  ```
- [ ] Playwright instalado (si se usa):
  ```bash
  playwright install chromium
  ```

### Verificación
- [ ] `requirements.txt` actualizado con todas las dependencias
- [ ] Versiones específicas en `requirements.txt` (recomendado)

## 🧹 5. LIMPIEZA DE ARCHIVOS

### Archivos a Eliminar Antes de Subir
- [ ] `db.sqlite3` (base de datos local)
- [ ] `__pycache__/` (caché de Python)
- [ ] `venv/` (entorno virtual - no subir)
- [ ] `*.pyc` (archivos compilados)
- [ ] Archivos de desarrollo:
  - `Acción.docx`
  - Scripts de desarrollo obsoletos
  - Archivos de prueba temporales

### Archivos a Mantener
- ✅ `requirements.txt`
- ✅ `manage.py`
- ✅ `config/` (configuración)
- ✅ `apps/` (código de la aplicación)
- ✅ `theme/` (tema y estáticos)
- ✅ `.gitignore`
- ✅ `README.md` (si existe)

## 🔧 6. CONFIGURACIÓN ESPECÍFICA

### Settings
- [ ] `config/settings.py` usa variables de entorno
- [ ] `config/settings_pythonanywhere.py` existe y está configurado
- [ ] `config/settings_production.py` existe para configuración adicional

### URLs
- [ ] `config/urls.py` configurado correctamente
- [ ] Todas las rutas funcionan
- [ ] Admin de Django accesible en `/django-admin/`

### Middleware
- [ ] `django_browser_reload` deshabilitado en producción (opcional)
- [ ] WhiteNoise configurado para archivos estáticos (si se usa)

## 📧 7. EMAIL (OPCIONAL)

### Configuración SMTP
- [ ] Variables de entorno configuradas:
  ```bash
  export EMAIL_HOST='smtp.gmail.com'
  export EMAIL_PORT='587'
  export EMAIL_USE_TLS='True'
  export EMAIL_HOST_USER='tu-email@gmail.com'
  export EMAIL_HOST_PASSWORD='tu-app-password'
  export DEFAULT_FROM_EMAIL='noreply@tudominio.com'
  ```

## 📊 8. LOGGING

### Configuración
- [ ] Logging configurado en `settings_production.py`
- [ ] Directorio `logs/` creado
- [ ] Rotación de logs configurada
- [ ] Nivel de logging apropiado (INFO/ERROR)

## 🧪 9. PRUEBAS

### Funcionalidades Principales
- [ ] Login/Logout funciona
- [ ] Dashboard carga correctamente
- [ ] Crear/Editar empresas funciona
- [ ] Crear/Editar empleados funciona
- [ ] Evaluaciones funcionan
- [ ] Generación de PDF funciona
- [ ] Generación de PowerPoint funciona
- [ ] Exportación a Excel funciona
- [ ] PWA funciona (offline mode)

### Rendimiento
- [ ] Páginas cargan en tiempo razonable
- [ ] Archivos estáticos se sirven correctamente
- [ ] No hay errores 500 en logs

## 🚀 10. DESPLIEGUE

### Pasos Finales
1. [ ] Subir código a PythonAnywhere (Git o manual)
2. [ ] Configurar variables de entorno en consola
3. [ ] Instalar dependencias
4. [ ] Ejecutar migraciones
5. [ ] Crear superusuario
6. [ ] Ejecutar `collectstatic`
7. [ ] Configurar Web App en PythonAnywhere
8. [ ] Configurar rutas estáticas
9. [ ] Reiniciar aplicación web
10. [ ] Verificar que el sitio funciona

### Verificación Post-Despliegue
- [ ] Sitio accesible: `https://tuusuario.pythonanywhere.com`
- [ ] Login funciona
- [ ] No hay errores en consola del navegador
- [ ] Archivos estáticos se cargan (CSS, JS, imágenes)
- [ ] HTTPS funciona correctamente
- [ ] Redirecciones funcionan

## ⚠️ 11. PROBLEMAS COMUNES

### Si hay errores de módulos no encontrados:
```bash
pip3.10 install --user nombre-del-modulo
```

### Si hay errores de archivos estáticos:
```bash
python3.10 manage.py collectstatic --noinput
```

### Si hay errores de base de datos:
- Verificar variables de entorno
- Verificar que la base de datos existe
- Verificar credenciales

### Si hay errores 500:
- Revisar logs en la pestaña "Web" de PythonAnywhere
- Verificar `DEBUG=False` en producción
- Revisar configuración de WSGI

## 📝 12. NOTAS ADICIONALES

### Limitaciones del Plan Gratuito
- Solo requests externos permitidos 00:00-08:00 UTC
- Playwright puede no funcionar en plan gratuito (requiere requests externos)
- Considerar plan Beginner ($5/mes) para producción real

### Mantenimiento
- Reiniciar aplicación después de cambios en código
- Ejecutar `collectstatic` después de cambios en archivos estáticos
- Hacer backups regulares de la base de datos

---

## ✅ VERIFICACIÓN FINAL

Antes de considerar el despliegue completo:

- [ ] Todas las casillas anteriores marcadas
- [ ] Pruebas realizadas exitosamente
- [ ] No hay errores en logs
- [ ] Sitio funciona correctamente
- [ ] Documentación actualizada

---

**Fecha de revisión:** _______________
**Revisado por:** _______________
**Estado:** ⬜ Pendiente | ⬜ En Progreso | ⬜ Completado

