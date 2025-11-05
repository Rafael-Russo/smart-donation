// Service Worker para Smart Donation PWA
// Versão: 1.0.0

const CACHE_NAME = 'smart-donation-v1';
const OFFLINE_URL = '/offline/';

// Arquivos essenciais para cache
const STATIC_CACHE_URLS = [
    '/',
    '/static/css/style.css',
    '/static/js/app.js',
    '/static/manifest.json',
    '/static/icons/icon-192x192.png',
    '/static/icons/icon-512x512.png',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css',
    'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js',
];

// Instalação do Service Worker
self.addEventListener('install', (event) => {
    console.log('[Service Worker] Instalando...');
    
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('[Service Worker] Cache aberto');
                return cache.addAll(STATIC_CACHE_URLS);
            })
            .catch((error) => {
                console.error('[Service Worker] Erro ao cachear arquivos:', error);
            })
    );
    
    // Força o Service Worker a se tornar ativo imediatamente
    self.skipWaiting();
});

// Ativação do Service Worker
self.addEventListener('activate', (event) => {
    console.log('[Service Worker] Ativando...');
    
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('[Service Worker] Removendo cache antigo:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    
    // Toma controle de todas as páginas imediatamente
    return self.clients.claim();
});

// Interceptação de requisições (Fetch)
self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);
    
    // Ignora requisições não-GET e de outros domínios (exceto CDNs)
    if (request.method !== 'GET') {
        return;
    }
    
    // Estratégia: Network First com Cache Fallback
    event.respondWith(
        fetch(request)
            .then((response) => {
                // Se a resposta for válida, clona e adiciona ao cache
                if (response && response.status === 200) {
                    const responseClone = response.clone();
                    
                    caches.open(CACHE_NAME).then((cache) => {
                        cache.put(request, responseClone);
                    });
                }
                
                return response;
            })
            .catch(() => {
                // Se falhar (offline), tenta buscar do cache
                return caches.match(request)
                    .then((cachedResponse) => {
                        if (cachedResponse) {
                            return cachedResponse;
                        }
                        
                        // Se não estiver no cache e for navegação HTML, retorna página offline
                        if (request.headers.get('accept').includes('text/html')) {
                            return caches.match(OFFLINE_URL);
                        }
                        
                        // Para outros recursos, retorna resposta vazia
                        return new Response('Recurso não disponível offline', {
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

// Sincronização em background (quando voltar online)
self.addEventListener('sync', (event) => {
    console.log('[Service Worker] Sincronizando em background...');
    
    if (event.tag === 'sync-data') {
        event.waitUntil(syncData());
    }
});

// Função auxiliar para sincronizar dados quando voltar online
async function syncData() {
    try {
        // Aqui você pode implementar lógica para sincronizar dados salvos offline
        console.log('[Service Worker] Dados sincronizados com sucesso');
    } catch (error) {
        console.error('[Service Worker] Erro ao sincronizar dados:', error);
    }
}

// Notificações Push (opcional)
self.addEventListener('push', (event) => {
    console.log('[Service Worker] Push recebido');
    
    const options = {
        body: event.data ? event.data.text() : 'Nova notificação',
        icon: '/static/icons/icon-192x192.png',
        badge: '/static/icons/badge-72x72.png',
        vibrate: [200, 100, 200],
        data: {
            dateOfArrival: Date.now(),
            primaryKey: 1
        },
        actions: [
            {
                action: 'explore',
                title: 'Ver mais',
                icon: '/static/icons/checkmark.png'
            },
            {
                action: 'close',
                title: 'Fechar',
                icon: '/static/icons/xmark.png'
            }
        ]
    };
    
    event.waitUntil(
        self.registration.showNotification('Smart Donation', options)
    );
});

// Click em notificação
self.addEventListener('notificationclick', (event) => {
    console.log('[Service Worker] Notificação clicada');
    
    event.notification.close();
    
    if (event.action === 'explore') {
        event.waitUntil(
            clients.openWindow('/')
        );
    }
});

// Mensagens do cliente
self.addEventListener('message', (event) => {
    console.log('[Service Worker] Mensagem recebida:', event.data);
    
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
});
