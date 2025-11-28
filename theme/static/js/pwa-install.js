/**
 * Manejo de instalación PWA
 */

let deferredPrompt;

window.addEventListener('beforeinstallprompt', (e) => {
    // Prevenir el prompt automático
    e.preventDefault();
    deferredPrompt = e;
    
    // Mostrar botón de instalación
    showInstallButton();
});

function showInstallButton() {
    // Crear botón de instalación si no existe
    if (document.getElementById('pwa-install-btn')) return;
    
    const installBtn = document.createElement('button');
    installBtn.id = 'pwa-install-btn';
    installBtn.className = 'fixed bottom-4 right-4 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg shadow-lg z-50 flex items-center gap-2';
    installBtn.innerHTML = `
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
        </svg>
        Instalar App
    `;
    
    installBtn.addEventListener('click', installPWA);
    document.body.appendChild(installBtn);
}

async function installPWA() {
    if (!deferredPrompt) {
        alert('La aplicación ya está instalada o no es compatible con tu navegador.');
        return;
    }
    
    // Mostrar el prompt
    deferredPrompt.prompt();
    
    // Esperar respuesta del usuario
    const { outcome } = await deferredPrompt.userChoice;
    
    if (outcome === 'accepted') {
        console.log('Usuario aceptó instalar la PWA');
        // Ocultar botón
        const btn = document.getElementById('pwa-install-btn');
        if (btn) btn.remove();
    }
    
    deferredPrompt = null;
}

// Verificar si ya está instalada
window.addEventListener('appinstalled', () => {
    console.log('PWA instalada');
    const btn = document.getElementById('pwa-install-btn');
    if (btn) btn.remove();
});

