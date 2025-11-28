# ⚡ PRUEBA RÁPIDA - Cambios Implementados

## 🚀 SERVIDOR INICIADO

El servidor está corriendo en: **http://127.0.0.1:8000**

---

## ✅ PASOS PARA PROBAR

### 1. Abrir la Aplicación
```
http://127.0.0.1:8000/login/
```

**Credenciales:**
- Email: `admin@test.com`
- Password: `admin123`

---

### 2. Verificar Service Worker (Modo Offline)

1. Presiona **F12** para abrir DevTools
2. Ve a la pestaña **Console**
3. Deberías ver: `✅ Service Worker registrado: http://127.0.0.1:8000/`
4. Ve a **Application** > **Service Workers** para confirmar

---

### 3. Probar Encriptación de Contraseñas

#### Como Superusuario:
1. Ve a **Empleados** > Selecciona cualquier empleado
2. Busca la sección "Contraseña"
3. ✅ Deberías ver la contraseña desencriptada
4. Ve a **Empresas** > Edita una empresa
5. ✅ Deberías ver la contraseña del administrador

#### Crear Usuario Nuevo:
1. Ve a **Empleados** > **Nuevo Empleado**
2. Completa el formulario y guarda
3. Verifica que la contraseña se muestra en los mensajes
4. Edita el empleado recién creado
5. ✅ Como superusuario, deberías ver la contraseña

---

### 4. Probar Modo Offline

1. Con la aplicación abierta, abre DevTools (F12)
2. Ve a la pestaña **Network**
3. En el dropdown, selecciona **Offline**
4. Recarga la página (F5)
5. ✅ Deberías ver el indicador amarillo: "⚠ Modo offline"
6. Navega por páginas ya visitadas (deberían funcionar)
7. Vuelve a poner **Online** en Network
8. ✅ El indicador debería desaparecer

---

### 5. Verificar UI/UX Mejorado

1. Redimensiona la ventana del navegador
2. ✅ Verifica que:
   - Los botones se adaptan (texto más corto en móvil)
   - El header se apila verticalmente en pantallas pequeñas
   - Las tabs tienen scroll horizontal si es necesario
   - Los elementos no se ven "apilados" o "demasiado grandes"
   - El texto es legible (no "opaco")

---

### 6. Verificar Validación de Seguridad

1. En la lista de empleados, prueba:
   - Búsqueda con caracteres especiales: `test<script>`
   - Filtro de año con valor inválido: `?year=abc`
   - Paginación con número inválido: `?per_page=999`
2. ✅ Verifica que no hay errores en la consola
3. ✅ Los valores inválidos se ignoran o se corrigen automáticamente

---

## 🔍 VERIFICACIONES EN CONSOLA

Abre la consola (F12 > Console) y verifica:

### ✅ Service Worker:
```
✅ Service Worker registrado: http://127.0.0.1:8000/
```

### ✅ Offline Manager:
Cuando desconectas internet:
```
[OfflineManager] Sin conexión
```

Cuando vuelve la conexión:
```
[OfflineManager] Conexión restaurada
```

### ❌ Sin Errores:
- No deberían aparecer errores en rojo
- Solo mensajes informativos

---

## 📋 CHECKLIST RÁPIDO

- [ ] Service Worker se registra correctamente
- [ ] Indicador offline aparece cuando no hay conexión
- [ ] Superusuario puede ver contraseñas desencriptadas
- [ ] Admin de empresa NO puede ver contraseñas
- [ ] Diseño responsive funciona bien
- [ ] Texto legible (no opaco)
- [ ] Validación de inputs funciona
- [ ] Sin errores en consola

---

## 🐛 SI HAY PROBLEMAS

### Service Worker no se registra:
- Verifica que estés en `http://127.0.0.1:8000` (no `localhost`)
- Revisa la consola para errores específicos

### Contraseñas no se muestran:
- Verifica que estés logueado como superusuario
- Verifica que el usuario tenga `stored_password` en la BD

### Modo offline no funciona:
- Verifica que el Service Worker esté registrado
- Limpia el cache: DevTools > Application > Clear storage

---

## 🎯 RESULTADO ESPERADO

Después de probar, deberías tener:
- ✅ Aplicación funcionando normalmente
- ✅ Service Worker activo
- ✅ Contraseñas encriptadas (solo superusuarios las ven)
- ✅ Modo offline funcionando
- ✅ Diseño responsive y compacto
- ✅ Sin errores

¡Listo para probar! 🚀

