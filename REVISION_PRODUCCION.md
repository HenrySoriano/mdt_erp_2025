# 📋 REVISIÓN EXHAUSTIVA PARA PRODUCCIÓN

## ✅ ARCHIVOS QUE DEBEN ELIMINARSE

### 🔴 CRÍTICO - Archivos Obsoletos

1. **`apps/presentation/views/admin_views_pptx.py`**
   - **Razón**: Está importado en `config/urls.py` pero NO se usa ninguna función
   - **Estado**: Todas las funciones de PowerPoint están ahora en `admin_views.py` usando Playwright
   - **Acción**: ELIMINAR y remover import de `urls.py`

2. **`debug_page.html`** (raíz)
   - **Razón**: Archivo de error de Django guardado accidentalmente
   - **Acción**: ELIMINAR

### 🟡 IMPORTANTE - Archivos de Desarrollo

3. **Scripts de utilidad** (raíz):
   - `create_superuser_and_load_data.py` - Solo para setup inicial
   - `restaurar_superusuario.py` - Solo para desarrollo
   - `update_question_explanations.py` - Ya ejecutado, no necesario
   - `update_stored_passwords.py` - Ya ejecutado, no necesario
   - **Acción**: Mover a carpeta `scripts/` o eliminar

4. **Scripts de activación redundantes**:
   - `ACTIVAR_ENTORNO.bat`
   - `ACTIVAR_ENTORNO.ps1`
   - `activar.ps1`
   - **Acción**: Mantener solo uno o eliminar todos (usar `venv\Scripts\activate`)

5. **`Acción.docx`** (raíz)
   - **Razón**: Archivo Word que no es parte del código
   - **Acción**: ELIMINAR o mover a documentación

### 🟢 MENOR - Fixtures Duplicados

6. **Fixtures antiguos** (`apps/infrastructure/fixtures/`):
   - `dimensions_updated.json` - Versión antigua
   - `questions_updated.json` - Versión antigua
   - `questions_final.json` - Posiblemente duplicado
   - **Acción**: Mantener solo `dimensions.json` y `questions.json` (versiones finales)

---

## ⚠️ ARCHIVOS VACÍOS (Arquitectura DDD no implementada)

Estos directorios están vacíos y son parte de una arquitectura DDD que no se implementó:

- `apps/domain/entities/__init__.py` - Vacío
- `apps/domain/interfaces/__init__.py` - Vacío
- `apps/infrastructure/repositories/__init__.py` - Vacío
- `apps/application/use_cases/__init__.py` - Vacío

**Recomendación**: 
- **Opción 1**: Eliminar estos directorios si no se van a usar
- **Opción 2**: Mantenerlos si planeas implementar DDD en el futuro

---

## ✅ ARCHIVOS QUE DEBEN MANTENERSE

### Archivos esenciales:
- ✅ Todos los modelos (`apps/infrastructure/models/`)
- ✅ Todas las vistas (`apps/presentation/views/`)
- ✅ Todos los templates (`apps/presentation/templates/`)
- ✅ Todas las migraciones (`apps/infrastructure/migrations/`)
- ✅ Configuración (`config/`)
- ✅ `requirements.txt`
- ✅ `manage.py`
- ✅ Fixtures finales: `dimensions.json` y `questions.json`

### Scripts útiles (opcional mantener):
- `INICIAR_SERVIDOR.ps1` - Útil para producción
- `INICIAR_TAILWIND.ps1` - Útil si se necesita recompilar CSS
- `EJECUTAR_PROYECTO.md` - Documentación útil
- `INICIO_RAPIDO.md` - Documentación útil
- `SOLUCION_POWERSHELL.md` - Documentación útil

---

## 🔧 ACCIONES RECOMENDADAS

### 1. Limpiar imports no usados

**Archivo**: `config/urls.py`
```python
# ELIMINAR esta línea (línea 20):
from apps.presentation.views import admin_views_pptx
```

### 2. Crear carpeta para scripts de desarrollo

```bash
mkdir scripts
# Mover scripts de desarrollo allí
```

### 3. Verificar que no haya referencias a archivos eliminados

Buscar referencias a:
- `admin_views_pptx`
- `download_admin_results_pptx` (función antigua)

---

## 📊 RESUMEN

| Categoría | Cantidad | Acción |
|-----------|----------|--------|
| Archivos obsoletos críticos | 2 | ELIMINAR |
| Scripts de desarrollo | 4 | Mover/Eliminar |
| Scripts redundantes | 3 | Eliminar duplicados |
| Fixtures duplicados | 3 | Eliminar versiones antiguas |
| Archivos vacíos (DDD) | 4 | Eliminar o mantener según plan |
| Archivo Word | 1 | Eliminar |

---

## ✅ CHECKLIST ANTES DE PRODUCCIÓN

- [ ] Eliminar `admin_views_pptx.py`
- [ ] Remover import de `admin_views_pptx` en `urls.py`
- [ ] Eliminar `debug_page.html`
- [ ] Eliminar o mover scripts de desarrollo
- [ ] Eliminar fixtures duplicados
- [ ] Eliminar `Acción.docx`
- [ ] Verificar que no haya errores de importación
- [ ] Ejecutar `python manage.py check`
- [ ] Ejecutar `python manage.py collectstatic` (si aplica)
- [ ] Verificar que todas las URLs funcionen
- [ ] Probar generación de PDF y PowerPoint

---

## 🚨 IMPORTANTE

**NO eliminar**:
- `db.sqlite3` (base de datos - aunque en producción usarás PostgreSQL/MySQL)
- `venv/` (entorno virtual - aunque no se sube a producción)
- `__pycache__/` (se regeneran automáticamente)
- Archivos `.pyc` (se regeneran automáticamente)

**En producción**:
- Usar base de datos PostgreSQL o MySQL
- Configurar `DEBUG = False` en `settings.py`
- Configurar `ALLOWED_HOSTS`
- Configurar variables de entorno para secretos
- Configurar servidor web (Nginx + Gunicorn/uWSGI)

