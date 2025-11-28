# 🧪 PROBAR CAMBIOS IMPLEMENTADOS

**Fecha:** 2025-11-27

---

## ✅ CAMBIOS IMPLEMENTADOS PARA PROBAR

1. ✅ **Encriptación de contraseñas** - Solo superusuarios pueden verlas
2. ✅ **Modo Offline (PWA)** - Funciona sin conexión a internet
3. ✅ **Mejoras de UI/UX** - Diseño más compacto y responsive
4. ✅ **Mejoras de seguridad** - Validación de inputs, configuración segura

---

## 🚀 INICIAR SERVIDOR

### Opción 1: Usando el entorno virtual directamente
```powershell
.\venv\Scripts\python.exe manage.py runserver
```

### Opción 2: Activar entorno y luego ejecutar
```powershell
# Si tienes problemas con la política de ejecución:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\venv\Scripts\Activate.ps1
python manage.py runserver
```

---

## 🧪 PRUEBAS A REALIZAR

### 1. ✅ Probar Encriptación de Contraseñas

#### Como Superusuario:
1. Inicia sesión como superusuario (`admin@test.com` / `admin123`)
2. Ve a **Empleados** > Selecciona un empleado
3. Verifica que puedes ver la contraseña desencriptada
4. Ve a **Empresas** > Edita una empresa
5. Verifica que puedes ver la contraseña del administrador

#### Como Admin de Empresa:
1. Inicia sesión como admin de empresa
2. Ve a **Empleados** > Selecciona un empleado
3. Verifica que NO puedes ver la contraseña (debe mostrar mensaje de advertencia)
4. Verifica que aparece: "⚠️ La contraseña está encriptada. Solo los superusuarios pueden verla."

#### Crear Nuevo Usuario:
1. Crea un nuevo empleado o empresa
2. Verifica que la contraseña se guarda encriptada en la BD
3. Como superusuario, verifica que puedes verla desencriptada

---

### 2. ✅ Probar Modo Offline (PWA)

#### Verificar Service Worker:
1. Abre la aplicación en Chrome/Edge
2. Presiona **F12** para abrir DevTools
3. Ve a **Application** > **Service Workers**
4. Deberías ver: "✅ Service Worker registrado"
5. Si hay errores, revisa la consola

#### Probar Modo Offline:
1. Con la aplicación abierta, abre DevTools (F12)
2. Ve a la pestaña **Network**
3. Selecciona **Offline** en el dropdown
4. Recarga la página (F5)
5. Deberías ver el indicador amarillo: "⚠ Modo offline"
6. Intenta navegar por páginas ya visitadas (deberían funcionar)
7. Vuelve a poner **Online** en Network
8. El indicador debería desaparecer

#### Probar Instalación PWA:
1. Abre la aplicación en Chrome/Edge
2. Busca el icono de instalación en la barra de direcciones
3. O espera a que aparezca el botón "Instalar App" (abajo a la derecha)
4. Haz clic en instalar
5. La app se abrirá como aplicación nativa

---

### 3. ✅ Probar Mejoras de UI/UX

#### Responsive Design:
1. Abre la aplicación en diferentes tamaños de ventana
2. Verifica que:
   - Los botones se adaptan (texto abreviado en móvil)
   - El header se apila verticalmente en móvil
   - Las tabs tienen scroll horizontal en móvil
   - Los elementos no se ven "apilados" o "demasiado grandes"

#### Páginas a Verificar:
- ✅ Dashboard (`/admin/dashboard/`)
- ✅ Lista de Empleados (`/admin/employees/`)
- ✅ Lista de Empresas (`/admin/companies/`)
- ✅ Resultados (`/admin/results/`)
- ✅ Login (`/login/`)

---

### 4. ✅ Probar Validación de Seguridad

#### Validación de Inputs:
1. En la lista de empleados, prueba:
   - Búsqueda con caracteres especiales
   - Filtros con valores inválidos
   - Paginación con números inválidos
2. Verifica que no hay errores en la consola

#### Validación de Permisos:
1. Como admin de empresa, intenta acceder a:
   - Empleados de otra empresa (debería denegar acceso)
   - Empresas que no gestionas (debería denegar acceso)
2. Verifica que aparecen mensajes de error apropiados

---

## 🔍 VERIFICACIONES EN CONSOLA

Abre la consola del navegador (F12 > Console) y verifica:

### Service Worker:
```
✅ Service Worker registrado: http://127.0.0.1:8000/
```

### Offline Manager:
```
[OfflineManager] Conexión restaurada
[OfflineManager] Sin conexión
```

### Sin Errores:
- No deberían aparecer errores en rojo
- Solo mensajes informativos en verde/azul

---

## 📋 CHECKLIST DE PRUEBAS

### Encriptación:
- [ ] Superusuario puede ver contraseñas
- [ ] Admin de empresa NO puede ver contraseñas
- [ ] Nuevas contraseñas se encriptan automáticamente
- [ ] Contraseñas existentes se pueden encriptar con el script

### Modo Offline:
- [ ] Service Worker se registra correctamente
- [ ] Indicador offline aparece cuando no hay conexión
- [ ] Páginas visitadas funcionan offline
- [ ] Datos se guardan localmente
- [ ] Sincronización funciona al volver conexión

### UI/UX:
- [ ] Diseño responsive en móvil
- [ ] Botones compactos y bien organizados
- [ ] Texto legible (no "opaco")
- [ ] Navegación fluida

### Seguridad:
- [ ] Inputs validados correctamente
- [ ] Permisos funcionan correctamente
- [ ] No hay errores de validación en consola

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### Service Worker no se registra:
```javascript
// En consola del navegador, ejecuta:
navigator.serviceWorker.getRegistrations().then(registrations => {
    console.log('Service Workers registrados:', registrations);
});
```

### Ver datos offline almacenados:
1. DevTools > Application > IndexedDB
2. Expande `mdt_erp_db`
3. Ver tablas: `evaluations`, `responses`, `sync_queue`

### Limpiar cache del Service Worker:
1. DevTools > Application > Storage
2. Haz clic en "Clear site data"
3. Recarga la página

### Verificar encriptación:
```python
# En el shell de Django:
python manage.py shell
>>> from apps.infrastructure.models import CustomUser
>>> user = CustomUser.objects.first()
>>> print(user.stored_password)  # Debería estar encriptado (texto largo)
>>> print(user.get_stored_password(user))  # Debería desencriptar (solo si eres superusuario)
```

---

## 🎯 RESULTADO ESPERADO

Después de todas las pruebas, deberías tener:
- ✅ Contraseñas encriptadas y solo visibles para superusuarios
- ✅ Aplicación funcionando offline
- ✅ Diseño responsive y compacto
- ✅ Validación de seguridad funcionando
- ✅ Sin errores en consola

¡Listo para probar! 🚀

