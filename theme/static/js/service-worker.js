/**
 * Service Worker para modo offline
 * Cachea recursos y permite trabajar sin conexión
 */

const CACHE_NAME = 'mdt-erp-v1';
const OFFLINE_PAGE = '/offline/';

// Recursos estáticos a cachear
const STATIC_ASSETS = [
    '/',
    '/static/css/output.css',
    '/static/js/app.js',
    '/offline/',
];

// Instalar Service Worker
self.addEventListener('install', (event) => {
    console.log('[Service Worker] Instalando...');
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            console.log('[Service Worker] Cacheando recursos estáticos');
            return cache.addAll(STATIC_ASSETS);
        })
    );
    self.skipWaiting();
});

// Activar Service Worker
self.addEventListener('activate', (event) => {
    console.log('[Service Worker] Activando...');
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('[Service Worker] Eliminando cache antiguo:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    return self.clients.claim();
});

// Interceptar solicitudes
self.addEventListener('fetch', (event) => {
    // Solo interceptar solicitudes GET
    if (event.request.method !== 'GET') {
        return;
    }

    // No cachear solicitudes a la API o endpoints dinámicos
    if (event.request.url.includes('/api/') || 
        event.request.url.includes('/admin/') ||
        event.request.url.includes('/generate-') ||
        event.request.url.includes('/download-')) {
        return;
    }

    event.respondWith(
        caches.match(event.request).then((response) => {
            // Si está en cache, retornarlo
            if (response) {
                return response;
            }

            // Intentar obtener de la red
            return fetch(event.request)
                .then((response) => {
                    // Si la respuesta es válida, cachearla
                    if (response && response.status === 200 && response.type === 'basic') {
                        const responseToCache = response.clone();
                        caches.open(CACHE_NAME).then((cache) => {
                            cache.put(event.request, responseToCache);
                        });
                    }
                    return response;
                })
                .catch(() => {
                    // Si falla y es una navegación, intentar mostrar página offline
                    if (event.request.mode === 'navigate') {
                        return caches.match(OFFLINE_PAGE).then((response) => {
                            if (response) {
                                return response;
                            }
                            // Si no hay página offline en cache, retornar respuesta básica
                            return new Response(
                                '<!DOCTYPE html><html><head><title>Sin Conexión</title></head><body><h1>Sin Conexión</h1><p>No hay conexión a internet. Por favor, verifica tu conexión.</p></body></html>',
                                {
                                    headers: { 'Content-Type': 'text/html' }
                                }
                            );
                        });
                    }
                    // Para otros recursos, retornar respuesta vacía
                    return new Response('Recurso no disponible offline', {
                        status: 503,
                        statusText: 'Service Unavailable',
                        headers: new Headers({
                            'Content-Type': 'text/plain'
                        })
                    });
                });
        })
    );
});

// Manejar mensajes del cliente
self.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
    
    if (event.data && event.data.type === 'CACHE_URLS') {
        event.waitUntil(
            caches.open(CACHE_NAME).then((cache) => {
                return cache.addAll(event.data.urls);
            })
        );
    }
});

