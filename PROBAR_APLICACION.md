# 🧪 COMANDOS PARA PROBAR LA APLICACIÓN

## 📋 PASO 1: Activar el Entorno Virtual

### Windows PowerShell:
```powershell
.\venv\Scripts\Activate.ps1
```

### Windows CMD:
```cmd
.\venv\Scripts\activate.bat
```

---

## 📋 PASO 2: Verificar el Proyecto

### Verificar configuración de Django:
```powershell
python manage.py check
```

**Resultado esperado**: `System check identified no issues (0 silenced).`

### Verificar migraciones pendientes:
```powershell
python manage.py showmigrations
```

**Si hay migraciones sin aplicar**, ejecuta:
```powershell
python manage.py migrate
```

---

## 📋 PASO 3: Cargar Datos Iniciales (Si es necesario)

### Cargar dimensiones y preguntas:
```powershell
python manage.py loaddata apps/infrastructure/fixtures/dimensions.json
python manage.py loaddata apps/infrastructure/fixtures/questions.json
```

**O usar el script de setup**:
```powershell
python scripts/create_superuser_and_load_data.py
```

---

## 📋 PASO 4: Iniciar el Servidor de Desarrollo

### Opción 1: Comando directo
```powershell
python manage.py runserver
```

### Opción 2: Usar el script PowerShell
```powershell
.\INICIAR_SERVIDOR.ps1
```

**El servidor iniciará en**: `http://127.0.0.1:8000`

---

## 📋 PASO 5: Iniciar Tailwind CSS (Si necesitas recompilar estilos)

### En una nueva terminal (con venv activado):
```powershell
python manage.py tailwind start
```

**Nota**: Solo necesario si modificas estilos CSS. Si ya están compilados, puedes omitir este paso.

---

## 🧪 CHECKLIST DE PRUEBAS

### ✅ Autenticación
1. **Login**: `http://127.0.0.1:8000/login/`
   - Usuario: `admin@test.com`
   - Contraseña: `admin123`

### ✅ Dashboard de Administrador
2. **Dashboard Admin**: `http://127.0.0.1:8000/admin/dashboard/`
   - Verificar que se muestre correctamente
   - Verificar nombre de empresa

### ✅ Gestión de Empleados
3. **Lista de Empleados**: `http://127.0.0.1:8000/admin/employees/`
   - Verificar lista
   - Probar filtros
   - Probar búsqueda
   - Probar edición inline de estado

4. **Crear Empleado**: `http://127.0.0.1:8000/admin/employees/create/`
   - Crear un empleado de prueba
   - Verificar campos: fecha de ingreso, área ERP, etc.

5. **Detalle de Empleado**: `http://127.0.0.1:8000/admin/employees/1/`
   - Verificar información completa
   - Verificar rango de edad calculado

### ✅ Gestión de Empresas
6. **Lista de Empresas**: `http://127.0.0.1:8000/admin/companies/`
   - Verificar lista
   - Crear/editar empresa

### ✅ Evaluaciones
7. **Tomar Evaluación**: `http://127.0.0.1:8000/employee/evaluation/start/`
   - Iniciar sesión como empleado
   - Completar evaluación
   - Verificar guardado

8. **Resultados de Empleado**: `http://127.0.0.1:8000/employee/evaluation/1/results/`
   - Verificar gráfico de dimensiones
   - Verificar recomendaciones
   - Probar descarga de PDF

### ✅ Resultados de Administrador
9. **Resultados Generales**: `http://127.0.0.1:8000/admin/results/`
   - Verificar gráfico principal
   - Verificar todas las pestañas:
     - ✅ Cumplimiento
     - 📊 Vista General
     - 👥 Género
     - 🎂 Edad
     - 🏢 Área
     - 📚 Educación
     - ⏱️ Antigüedad
     - 🌍 Etnia
     - 📍 Ubicación
   - Verificar recomendaciones en cada pestaña

10. **Previsualizar PowerPoint**: `http://127.0.0.1:8000/admin/results/company/1/preview-pptx/?year=2025`
    - Verificar que todos los gráficos se muestren
    - Probar descarga de PowerPoint

11. **Previsualizar PDF**: `http://127.0.0.1:8000/admin/results/company/1/preview-pdf/?year=2025`
    - Verificar contenido completo
    - Probar generación de PDF

12. **Descargar Excel Anónimo**: `http://127.0.0.1:8000/admin/results/excel-anonymous/?year=2025`
    - Verificar estructura del Excel
    - Verificar anonimato

### ✅ Importación/Exportación
13. **Importación Masiva**: `http://127.0.0.1:8000/admin/bulk-import/`
    - Descargar plantilla
    - Probar importación

14. **Exportación**: Desde lista de empleados
    - Probar exportar a Excel
    - Probar exportar a CSV

---

## 🔍 VERIFICACIONES ADICIONALES

### Verificar que no haya errores en consola:
- Revisar la terminal donde corre el servidor
- No debe haber errores 500, 404 críticos

### Verificar paleta de colores:
- Todos los elementos deben usar la paleta azul corporativo
- Los gráficos de riesgo deben mantener rojo/amarillo/verde

### Verificar responsividad:
- Probar en diferentes tamaños de pantalla
- Verificar que los gráficos se adapten

---

## 🚨 COMANDOS DE DIAGNÓSTICO

### Si hay errores, ejecutar:

```powershell
# Verificar configuración
python manage.py check --deploy

# Ver migraciones aplicadas
python manage.py showmigrations

# Limpiar caché de Python
Get-ChildItem -Path . -Include __pycache__ -Recurse -Force | Remove-Item -Force -Recurse

# Verificar dependencias
pip list
```

---

## 📝 NOTAS IMPORTANTES

1. **Base de datos**: Actualmente usa SQLite (`db.sqlite3`). En producción cambiar a PostgreSQL/MySQL.

2. **DEBUG**: En producción, cambiar `DEBUG = False` en `config/settings.py`.

3. **ALLOWED_HOSTS**: En producción, agregar tu dominio en `ALLOWED_HOSTS`.

4. **Secret Key**: En producción, usar variable de entorno para `SECRET_KEY`.

5. **Archivos estáticos**: En producción, ejecutar `python manage.py collectstatic`.

---

## ✅ RESULTADO ESPERADO

Si todas las pruebas pasan correctamente:
- ✅ Login funciona
- ✅ Dashboards se muestran correctamente
- ✅ CRUD de empleados funciona
- ✅ Evaluaciones se pueden completar
- ✅ Resultados se muestran correctamente
- ✅ Gráficos se renderizan bien
- ✅ PDF y PowerPoint se generan correctamente
- ✅ Excel se descarga correctamente
- ✅ Paleta de colores aplicada correctamente

**¡El proyecto está listo para producción!** 🚀

