# 📱 MODO OFFLINE IMPLEMENTADO - PWA

**Fecha:** 2025-11-27  
**Estado:** ✅ Implementado

---

## ✅ IMPLEMENTACIÓN COMPLETA

Se ha implementado una **Progressive Web App (PWA)** que permite trabajar offline usando Service Workers, IndexedDB y sincronización automática.

---

## 🔧 COMPONENTES IMPLEMENTADOS

### 1. ✅ Service Worker
**Archivo:** `theme/static/js/service-worker.js`

- Cachea recursos estáticos (CSS, JS, imágenes)
- Intercepta solicitudes y sirve desde cache cuando está offline
- Muestra página offline cuando no hay conexión
- Actualiza cache automáticamente

### 2. ✅ Offline Manager
**Archivo:** `theme/static/js/offline-manager.js`

- Detecta estado online/offline
- Almacena datos localmente en IndexedDB
- Sincroniza automáticamente cuando vuelve la conexión
- Muestra notificaciones de estado

### 3. ✅ PWA Install
**Archivo:** `theme/static/js/pwa-install.js`

- Maneja instalación de la PWA
- Muestra botón de instalación cuando está disponible
- Detecta si la app ya está instalada

### 4. ✅ Manifest.json
**Archivo:** `theme/static/manifest.json`

- Configuración de la PWA
- Iconos y metadatos
- Permite instalación como app nativa

### 5. ✅ Página Offline
**Archivo:** `apps/presentation/templates/offline.html`

- Página mostrada cuando no hay conexión
- Informa qué funciones están disponibles
- Botón para reintentar conexión

### 6. ✅ Vistas Offline
**Archivo:** `apps/presentation/views/offline_views.py`

- `offline_page()` - Renderiza página offline
- `manifest_view()` - Sirve manifest.json
- `service_worker_view()` - Sirve service-worker.js

---

## 📋 FUNCIONALIDADES OFFLINE

### ✅ Disponibles Offline:
1. **Navegación** - Páginas previamente visitadas
2. **Visualización** - Ver datos ya cargados
3. **Formularios** - Completar evaluaciones (se guardan localmente)
4. **Datos Locales** - Trabajar con información en IndexedDB

### ❌ No Disponibles Offline:
1. **Generación de Reportes** - PDF/PowerPoint requieren servidor
2. **Descargas** - Requieren conexión al servidor
3. **Sincronización** - Solo cuando hay conexión
4. **Autenticación** - Requiere validación en servidor

---

## 🚀 CONFIGURACIÓN

### 1. Instalar dependencias (ya incluidas):
No se requieren dependencias adicionales, todo usa APIs nativas del navegador.

### 2. Crear iconos PWA:
Necesitas crear iconos en diferentes tamaños en `theme/static/images/`:
- `icon-72x72.png`
- `icon-96x96.png`
- `icon-128x128.png`
- `icon-144x144.png`
- `icon-152x152.png`
- `icon-192x192.png`
- `icon-384x384.png`
- `icon-512x512.png`

**Nota:** Puedes usar un generador online como [PWA Asset Generator](https://github.com/onderceylan/pwa-asset-generator)

### 3. Configurar HTTPS (requerido para PWA):
Las PWA requieren HTTPS en producción. En desarrollo local, `localhost` funciona sin HTTPS.

---

## 📱 USO

### Instalación:
1. Abre la aplicación en el navegador
2. Aparecerá un botón "Instalar App" (o el navegador mostrará un prompt)
3. Haz clic en instalar
4. La app se instalará como aplicación nativa

### Modo Offline:
1. La app detecta automáticamente cuando no hay conexión
2. Muestra indicador de estado en la parte superior
3. Los datos se guardan localmente en IndexedDB
4. Cuando vuelve la conexión, se sincronizan automáticamente

### Sincronización:
- Automática cuando se restaura la conexión
- Manual desde el indicador de estado
- Los datos pendientes se marcan visualmente

---

## 🔧 PERSONALIZACIÓN

### Modificar recursos cacheados:
Edita `theme/static/js/service-worker.js` y modifica el array `STATIC_ASSETS`:

```javascript
const STATIC_ASSETS = [
    '/',
    '/static/css/output.css',
    '/static/js/app.js',
    '/offline/',
    // Añade más URLs aquí
];
```

### Modificar almacenamiento local:
Edita `theme/static/js/offline-manager.js` para añadir más stores en IndexedDB o modificar la lógica de sincronización.

### Personalizar manifest:
Edita `theme/static/manifest.json` para cambiar nombre, colores, iconos, etc.

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### Service Worker no se registra:
- Verifica que estés usando HTTPS (o localhost)
- Revisa la consola del navegador para errores
- Verifica que el archivo `service-worker.js` esté accesible

### Los datos no se sincronizan:
- Verifica que haya conexión a internet
- Revisa la consola para errores de sincronización
- Verifica que los endpoints de sincronización estén disponibles

### La app no se puede instalar:
- Verifica que el manifest.json sea válido
- Asegúrate de tener iconos en todos los tamaños requeridos
- Verifica que estés usando HTTPS (en producción)

### Los datos offline no persisten:
- Verifica que IndexedDB esté habilitado en el navegador
- Revisa la consola para errores de IndexedDB
- Verifica permisos del navegador

---

## 📚 REFERENCIAS

- [MDN - Service Workers](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API)
- [MDN - IndexedDB](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API)
- [Web.dev - PWA](https://web.dev/progressive-web-apps/)
- [Workbox](https://developers.google.com/web/tools/workbox) - Librería avanzada para Service Workers

---

## ✅ PRÓXIMOS PASOS (Opcional)

1. **Sincronización bidireccional** - Sincronizar cambios del servidor también
2. **Conflictos de datos** - Manejar cuando hay cambios offline y online
3. **Notificaciones push** - Notificar cuando hay actualizaciones
4. **Background sync** - Sincronizar en segundo plano
5. **Cache más inteligente** - Cachear más recursos dinámicamente

---

## 🎯 RESULTADO

La aplicación ahora puede:
- ✅ Funcionar sin conexión a internet
- ✅ Instalarse como app nativa
- ✅ Guardar datos localmente
- ✅ Sincronizar automáticamente cuando vuelve la conexión
- ✅ Mostrar estado de conexión
- ✅ Cachear recursos para acceso rápido

¡La aplicación está lista para trabajar online y offline! 🎉

