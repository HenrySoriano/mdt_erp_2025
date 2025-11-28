# 📱 INSTRUCCIONES PARA USO OFFLINE

## ✅ IMPLEMENTACIÓN COMPLETA

La aplicación ahora funciona **online y offline** usando tecnología PWA (Progressive Web App).

---

## 🚀 CÓMO FUNCIONA

### Modo Online (Con Internet):
- ✅ Funciona normalmente
- ✅ Todos los datos se sincronizan con el servidor
- ✅ Puedes generar reportes PDF/PowerPoint
- ✅ Puedes descargar archivos

### Modo Offline (Sin Internet):
- ✅ Puedes navegar por páginas previamente visitadas
- ✅ Puedes ver datos ya cargados
- ✅ Puedes completar evaluaciones (se guardan localmente)
- ✅ Los datos se sincronizan automáticamente cuando vuelve la conexión
- ❌ No puedes generar reportes (requieren servidor)
- ❌ No puedes descargar archivos nuevos

---

## 📱 INSTALAR COMO APP

### En Chrome/Edge (Desktop):
1. Abre la aplicación en el navegador
2. Busca el icono de instalación en la barra de direcciones (o menú)
3. Haz clic en "Instalar"
4. La app se instalará como aplicación nativa

### En Chrome (Android):
1. Abre la aplicación
2. Aparecerá un banner "Agregar a pantalla de inicio"
3. Toca "Agregar"
4. La app aparecerá en tu pantalla de inicio

### En Safari (iOS):
1. Abre la aplicación
2. Toca el botón de compartir
3. Selecciona "Agregar a pantalla de inicio"
4. La app aparecerá en tu pantalla de inicio

---

## 🔧 CONFIGURACIÓN REQUERIDA

### 1. Crear Iconos PWA:
Necesitas crear iconos en `theme/static/images/`:
- Ver archivo `CREAR_ICONOS_PWA.md` para instrucciones detalladas
- Mínimo requerido: `icon-192x192.png` y `icon-512x512.png`

### 2. Verificar Service Worker:
1. Abre las herramientas de desarrollador (F12)
2. Ve a la pestaña "Application" > "Service Workers"
3. Deberías ver el Service Worker registrado
4. Si hay errores, revisa la consola

---

## 🧪 PROBAR MODO OFFLINE

### Método 1: Desconectar Internet
1. Desconecta tu conexión WiFi/Ethernet
2. Recarga la página
3. Deberías ver el indicador "⚠ Modo offline" en la parte superior
4. Puedes navegar por páginas ya visitadas

### Método 2: Chrome DevTools
1. Abre DevTools (F12)
2. Ve a "Network" tab
3. Selecciona "Offline" en el dropdown
4. Recarga la página
5. Verás el modo offline activo

---

## 📊 ALMACENAMIENTO LOCAL

Los datos se guardan en **IndexedDB** del navegador:

### Datos Almacenados:
- Evaluaciones completadas offline
- Respuestas a preguntas
- Datos de sincronización pendiente

### Ver Datos Almacenados:
1. Abre DevTools (F12)
2. Ve a "Application" > "IndexedDB" > "mdt_erp_db"
3. Puedes ver las tablas: `evaluations`, `responses`, `sync_queue`

### Limpiar Datos:
1. DevTools > Application > Storage
2. Haz clic en "Clear site data"
3. Esto eliminará todos los datos offline

---

## 🔄 SINCRONIZACIÓN

### Automática:
- Cuando vuelve la conexión, se sincroniza automáticamente
- Verás una notificación: "Conexión restaurada. Sincronizando datos..."

### Manual:
- Los datos pendientes se sincronizan en el próximo acceso online
- No necesitas hacer nada especial

---

## ⚠️ LIMITACIONES

### No Disponible Offline:
1. **Autenticación** - Requiere servidor para validar credenciales
2. **Generación de Reportes** - PDF/PowerPoint requieren procesamiento en servidor
3. **Descargas** - Requieren conexión al servidor
4. **Datos Nuevos** - No se pueden obtener datos nuevos del servidor

### Disponible Offline:
1. **Navegación** - Páginas previamente visitadas
2. **Visualización** - Ver datos ya cargados
3. **Formularios** - Completar evaluaciones (se guardan localmente)
4. **Datos Locales** - Trabajar con información en IndexedDB

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### El Service Worker no se registra:
- Verifica que estés usando HTTPS (o localhost)
- Revisa la consola para errores
- Verifica que el archivo `service-worker.js` exista

### Los datos no se sincronizan:
- Verifica que haya conexión a internet
- Revisa la consola para errores
- Verifica que los endpoints de sincronización estén disponibles

### La app no se puede instalar:
- Verifica que el manifest.json sea válido
- Asegúrate de tener iconos en todos los tamaños requeridos
- Verifica que estés usando HTTPS (en producción)

### El indicador offline no aparece:
- Verifica que `offline-manager.js` esté cargado
- Revisa la consola para errores
- Verifica que el elemento `#offline-status` exista en el HTML

---

## 📚 REFERENCIAS

- [MDN - Service Workers](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API)
- [MDN - IndexedDB](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API)
- [Web.dev - PWA](https://web.dev/progressive-web-apps/)

---

## ✅ VERIFICACIÓN RÁPIDA

1. ✅ Abre la aplicación
2. ✅ Verifica en consola: "✅ Service Worker registrado"
3. ✅ Desconecta internet
4. ✅ Verifica que aparece "⚠ Modo offline"
5. ✅ Recarga la página (debería funcionar)
6. ✅ Reconecta internet
7. ✅ Verifica que desaparece el indicador offline

¡La aplicación está lista para trabajar offline! 🎉

