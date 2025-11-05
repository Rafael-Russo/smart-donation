// Smart Donation - JavaScript Principal
// PWA e funcionalidades interativas

// ========================================
// 1. REGISTRO DO SERVICE WORKER
// ========================================
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/static/sw.js')
            .then((registration) => {
                console.log('✅ Service Worker registrado com sucesso:', registration.scope);
                
                // Verifica atualizações do Service Worker
                registration.addEventListener('updatefound', () => {
                    const newWorker = registration.installing;
                    
                    newWorker.addEventListener('statechange', () => {
                        if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                            // Nova versão disponível
                            showUpdateNotification();
                        }
                    });
                });
            })
            .catch((error) => {
                console.error('❌ Erro ao registrar Service Worker:', error);
            });
    });
}

// ========================================
// 2. PROMPT DE INSTALAÇÃO PWA (Botão Flutuante)
// ========================================
let deferredPrompt;
let installButton;

window.addEventListener('beforeinstallprompt', (e) => {
    // Previne o prompt automático
    e.preventDefault();
    deferredPrompt = e;
    
    // Mostra o botão flutuante de instalação
    showFloatingInstallButton();
});

// Detecta quando o app já está instalado
window.addEventListener('appinstalled', () => {
    console.log('✅ PWA instalado com sucesso!');
    hideFloatingInstallButton();
    deferredPrompt = null;
});

function showFloatingInstallButton() {
    // Não mostrar se já estiver instalado
    if (isAppInstalled()) {
        return;
    }
    
    // Cria o botão flutuante se não existir
    if (!installButton) {
        installButton = document.createElement('button');
        installButton.className = 'pwa-install-button';
        installButton.setAttribute('aria-label', 'Instalar aplicativo');
        installButton.innerHTML = `
            <i class="bi bi-download"></i>
            <span class="pwa-install-button-tooltip">Instalar App</span>
        `;
        
        installButton.addEventListener('click', handleInstallClick);
        document.body.appendChild(installButton);
        
        console.log('📱 Botão de instalação PWA exibido');
    }
}

function hideFloatingInstallButton() {
    if (installButton) {
        installButton.classList.add('hidden');
        setTimeout(() => {
            if (installButton && installButton.parentNode) {
                installButton.parentNode.removeChild(installButton);
            }
            installButton = null;
        }, 300);
    }
}

async function handleInstallClick() {
    if (!deferredPrompt) {
        console.log('⚠️ Prompt de instalação não disponível');
        return;
    }
    
    // Mostra o prompt de instalação
    deferredPrompt.prompt();
    
    // Aguarda a escolha do usuário
    const { outcome } = await deferredPrompt.userChoice;
    
    console.log(`👤 Usuário ${outcome === 'accepted' ? 'aceitou' : 'recusou'} a instalação`);
    
    if (outcome === 'accepted') {
        hideFloatingInstallButton();
    }
    
    deferredPrompt = null;
}

function isAppInstalled() {
    // Verifica se está rodando em modo standalone (instalado)
    if (window.matchMedia('(display-mode: standalone)').matches) {
        return true;
    }
    
    // Verifica no iOS
    if (window.navigator.standalone === true) {
        return true;
    }
    
    // Verifica via document.referrer no Android
    if (document.referrer.includes('android-app://')) {
        return true;
    }
    
    return false;
}

// Esconde o botão se já estiver instalado
if (isAppInstalled()) {
    console.log('✅ App já está instalado');
} else {
    console.log('📱 App não está instalado - botão de instalação disponível');
}

// ========================================
// 3. DETECÇÃO DE CONEXÃO (ONLINE/OFFLINE)
// ========================================
function updateOnlineStatus() {
    const isOnline = navigator.onLine;
    const offlineBanner = document.getElementById('offline-banner');
    
    if (!isOnline) {
        if (!offlineBanner) {
            const banner = document.createElement('div');
            banner.id = 'offline-banner';
            banner.className = 'pwa-offline-banner';
            banner.innerHTML = `
                <i class="bi bi-wifi-off"></i>
                <strong>Você está offline</strong> - Algumas funcionalidades podem não estar disponíveis
            `;
            document.body.appendChild(banner);
        }
    } else {
        if (offlineBanner) {
            offlineBanner.remove();
            
            // Tenta sincronizar dados quando voltar online
            if ('serviceWorker' in navigator && 'sync' in ServiceWorkerRegistration.prototype) {
                navigator.serviceWorker.ready.then((registration) => {
                    return registration.sync.register('sync-data');
                }).catch((error) => {
                    console.error('Erro ao registrar sync:', error);
                });
            }
        }
    }
}

window.addEventListener('online', updateOnlineStatus);
window.addEventListener('offline', updateOnlineStatus);

// Verifica status inicial
document.addEventListener('DOMContentLoaded', updateOnlineStatus);

// ========================================
// 4. NOTIFICAÇÃO DE ATUALIZAÇÃO
// ========================================
function showUpdateNotification() {
    const updateBanner = document.createElement('div');
    updateBanner.className = 'alert alert-info position-fixed top-0 start-50 translate-middle-x mt-3';
    updateBanner.style.zIndex = '9999';
    updateBanner.innerHTML = `
        <i class="bi bi-arrow-repeat"></i>
        <strong>Nova versão disponível!</strong>
        <button class="btn btn-sm btn-info ms-2" onclick="window.location.reload()">
            Atualizar Agora
        </button>
    `;
    
    document.body.appendChild(updateBanner);
    
    // Remove após 10 segundos
    setTimeout(() => {
        updateBanner.remove();
    }, 10000);
}

// ========================================
// 5. MELHORIAS DE UI/UX
// ========================================

// Fade-in de cards ao carregar
document.addEventListener('DOMContentLoaded', () => {
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('fade-in');
        }, index * 50);
    });
});

// Confirmação antes de excluir
document.querySelectorAll('[data-confirm]').forEach((element) => {
    element.addEventListener('click', (e) => {
        const message = element.getAttribute('data-confirm');
        if (!confirm(message)) {
            e.preventDefault();
        }
    });
});

// Auto-hide de alerts após 5 segundos
document.addEventListener('DOMContentLoaded', () => {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach((alert) => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});

// ========================================
// 6. LAZY LOADING DE IMAGENS
// ========================================
document.addEventListener('DOMContentLoaded', () => {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach((img) => imageObserver.observe(img));
});

// ========================================
// 7. COMPARTILHAMENTO WEB SHARE API
// ========================================
function shareContent(title, text, url) {
    if (navigator.share) {
        navigator.share({
            title: title,
            text: text,
            url: url
        })
        .then(() => console.log('Conteúdo compartilhado com sucesso'))
        .catch((error) => console.error('Erro ao compartilhar:', error));
    } else {
        // Fallback: copiar link para clipboard
        navigator.clipboard.writeText(url)
            .then(() => {
                alert('Link copiado para a área de transferência!');
            });
    }
}

// Expõe função globalmente
window.shareContent = shareContent;

// ========================================
// 8. DEBOUNCE PARA BUSCAS
// ========================================
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Aplicar debounce em campos de busca
document.addEventListener('DOMContentLoaded', () => {
    const searchInputs = document.querySelectorAll('input[type="search"], input[name*="search"]');
    
    searchInputs.forEach((input) => {
        input.addEventListener('input', debounce((e) => {
            console.log('Buscando:', e.target.value);
            // Implementar lógica de busca aqui
        }, 300));
    });
});

// ========================================
// 9. TRATAMENTO DE ERROS DE IMAGEM
// ========================================
document.addEventListener('DOMContentLoaded', () => {
    const images = document.querySelectorAll('img');
    
    images.forEach((img) => {
        img.addEventListener('error', function() {
            this.src = '/static/images/placeholder.png';
            this.alt = 'Imagem não disponível';
        });
    });
});

// ========================================
// 10. ANALYTICS E TRACKING (OPCIONAL)
// ========================================
function trackEvent(category, action, label) {
    console.log('Track Event:', { category, action, label });
    
    // Integrar com Google Analytics ou similar
    if (typeof gtag !== 'undefined') {
        gtag('event', action, {
            'event_category': category,
            'event_label': label
        });
    }
}

window.trackEvent = trackEvent;

// ========================================
// 11. PERFORMANCE MONITORING
// ========================================
if ('PerformanceObserver' in window) {
    const observer = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
            console.log('Performance:', entry.name, entry.duration + 'ms');
        }
    });
    
    observer.observe({ entryTypes: ['navigation', 'resource'] });
}

console.log('✅ Smart Donation App inicializado!');
