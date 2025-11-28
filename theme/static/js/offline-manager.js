/**
 * Gestor de modo offline
 * Maneja almacenamiento local y sincronización
 */

class OfflineManager {
    constructor() {
        this.dbName = 'mdt_erp_db';
        this.dbVersion = 1;
        this.db = null;
        this.isOnline = navigator.onLine;
        this.syncQueue = [];
        
        this.init();
    }

    async init() {
        // Inicializar IndexedDB
        await this.initDB();
        
        // Escuchar cambios de conexión
        window.addEventListener('online', () => this.handleOnline());
        window.addEventListener('offline', () => this.handleOffline());
        
        // Verificar estado inicial
        this.updateOnlineStatus();
        
        // Intentar sincronizar si hay conexión
        if (this.isOnline) {
            this.syncPendingData();
        }
    }

    async initDB() {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open(this.dbName, this.dbVersion);
            
            request.onerror = () => reject(request.error);
            request.onsuccess = () => {
                this.db = request.result;
                resolve(this.db);
            };
            
            request.onupgradeneeded = (event) => {
                const db = event.target.result;
                
                // Store para evaluaciones pendientes
                if (!db.objectStoreNames.contains('evaluations')) {
                    const evaluationsStore = db.createObjectStore('evaluations', { keyPath: 'id', autoIncrement: true });
                    evaluationsStore.createIndex('employee_id', 'employee_id', { unique: false });
                    evaluationsStore.createIndex('status', 'status', { unique: false });
                }
                
                // Store para respuestas pendientes
                if (!db.objectStoreNames.contains('responses')) {
                    const responsesStore = db.createObjectStore('responses', { keyPath: 'id', autoIncrement: true });
                    responsesStore.createIndex('evaluation_id', 'evaluation_id', { unique: false });
                }
                
                // Store para datos de sincronización
                if (!db.objectStoreNames.contains('sync_queue')) {
                    const syncStore = db.createObjectStore('sync_queue', { keyPath: 'id', autoIncrement: true });
                    syncStore.createIndex('type', 'type', { unique: false });
                    syncStore.createIndex('status', 'status', { unique: false });
                }
            };
        });
    }

    updateOnlineStatus() {
        this.isOnline = navigator.onLine;
        const statusElement = document.getElementById('offline-status');
        
        if (statusElement) {
            if (this.isOnline) {
                statusElement.classList.add('hidden');
            } else {
                statusElement.classList.remove('hidden');
            }
        }
    }

    handleOnline() {
        console.log('[OfflineManager] Conexión restaurada');
        this.isOnline = true;
        this.updateOnlineStatus();
        this.showNotification('Conexión restaurada. Sincronizando datos...', 'success');
        this.syncPendingData();
    }

    handleOffline() {
        console.log('[OfflineManager] Sin conexión');
        this.isOnline = false;
        this.updateOnlineStatus();
        this.showNotification('Sin conexión. Trabajando en modo offline...', 'warning');
    }

    showNotification(message, type = 'info') {
        // Crear notificación visual
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 ${
            type === 'success' ? 'bg-green-500 text-white' :
            type === 'warning' ? 'bg-yellow-500 text-yellow-900' :
            'bg-blue-500 text-white'
        }`;
        notification.textContent = message;
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    // Guardar evaluación localmente
    async saveEvaluationLocal(evaluationData) {
        if (!this.db) await this.initDB();
        
        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction(['evaluations'], 'readwrite');
            const store = transaction.objectStore('evaluations');
            
            const data = {
                ...evaluationData,
                synced: false,
                created_at: new Date().toISOString()
            };
            
            const request = store.add(data);
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }

    // Guardar respuesta localmente
    async saveResponseLocal(responseData) {
        if (!this.db) await this.initDB();
        
        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction(['responses'], 'readwrite');
            const store = transaction.objectStore('responses');
            
            const data = {
                ...responseData,
                synced: false,
                created_at: new Date().toISOString()
            };
            
            const request = store.add(data);
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }

    // Obtener evaluaciones locales
    async getLocalEvaluations() {
        if (!this.db) await this.initDB();
        
        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction(['evaluations'], 'readonly');
            const store = transaction.objectStore('evaluations');
            const request = store.getAll();
            
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }

    // Sincronizar datos pendientes
    async syncPendingData() {
        if (!this.isOnline || !this.db) return;
        
        try {
            // Sincronizar evaluaciones
            const evaluations = await this.getLocalEvaluations();
            const unsynced = evaluations.filter(e => !e.synced);
            
            for (const evaluation of unsynced) {
                try {
                    await this.syncEvaluation(evaluation);
                } catch (error) {
                    console.error('[OfflineManager] Error sincronizando evaluación:', error);
                }
            }
            
            this.showNotification(`Sincronizadas ${unsynced.length} evaluaciones`, 'success');
        } catch (error) {
            console.error('[OfflineManager] Error en sincronización:', error);
        }
    }

    // Sincronizar una evaluación
    async syncEvaluation(evaluation) {
        // Aquí harías la llamada al servidor
        // Por ahora solo marcamos como sincronizada
        const transaction = this.db.transaction(['evaluations'], 'readwrite');
        const store = transaction.objectStore('evaluations');
        evaluation.synced = true;
        await store.put(evaluation);
    }

    // Verificar si hay datos pendientes
    async hasPendingData() {
        if (!this.db) return false;
        
        const evaluations = await this.getLocalEvaluations();
        return evaluations.some(e => !e.synced);
    }
}

// Instancia global
window.offlineManager = new OfflineManager();

