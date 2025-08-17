// Funcionalidades para página de download

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar todas as funcionalidades
    initDownloadAnimation();
    initFloatingElements();
    initButtonEffects();
    initProgressBar();
});


// Animação de texto de download
function initDownloadAnimation() {
    const downloadText = document.querySelector('.download-text');
    
    if (!downloadText) return;
    
    const texts = ['Baixando', 'Baixando.', 'Baixando..', 'Baixando...'];
    let index = 0;
    
    // Atualizar texto a cada 500ms
    const textInterval = setInterval(() => {
        downloadText.textContent = texts[index];
        index = (index + 1) % texts.length;
    }, 500);
    
    // Parar animação após 10 segundos (simulando fim do download)
    setTimeout(() => {
        clearInterval(textInterval);
        downloadText.textContent = 'Concluído!';
        downloadText.style.color = '#48bb78';
    }, 10000);
}


// Animação dos elementos flutuantes
function initFloatingElements() {
    const circles = document.querySelectorAll('.floating-circle');
    
    circles.forEach((circle, index) => {
        // Adicionar movimento aleatório sutil
        setInterval(() => {
            const randomX = Math.random() * 10 - 5;
            const randomY = Math.random() * 10 - 5;
            
            circle.style.transform = `translate(${randomX}px, ${randomY}px)`;
        }, 2000 + index * 500);
    });
}


// Efeitos nos botões
function initButtonEffects() {
    const ctaButton = document.querySelector('.cta-button');
    const signInBtn = document.querySelector('.sign-in-btn');
    
    // Efeito de ripple no botão CTA
    if (ctaButton) {
        ctaButton.addEventListener('click', function(e) {
            createRippleEffect(e, this);
        });
    }
    
    // Efeito de feedback no botão de login
    if (signInBtn) {
        signInBtn.addEventListener('click', function(e) {
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
        });
    }
}


// Criar efeito ripple
function createRippleEffect(event, element) {
    const ripple = document.createElement('span');
    const rect = element.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = event.clientX - rect.left - size / 2;
    const y = event.clientY - rect.top - size / 2;
    
    ripple.style.cssText = `
        position: absolute;
        width: ${size}px;
        height: ${size}px;
        left: ${x}px;
        top: ${y}px;
        background: rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        transform: scale(0);
        animation: ripple 0.6s ease-out;
        pointer-events: none;
    `;
    
    element.style.position = 'relative';
    element.style.overflow = 'hidden';
    element.appendChild(ripple);
    
    // Remover ripple após animação
    setTimeout(() => {
        ripple.remove();
    }, 600);
}


// Barra de progresso simulada
function initProgressBar() {
    const laptopScreen = document.querySelector('.laptop-screen');
    
    if (!laptopScreen) return;
    
    // Criar barra de progresso
    const progressContainer = document.createElement('div');
    progressContainer.className = 'progress-container';
    progressContainer.style.cssText = `
        position: absolute;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        width: 80%;
        height: 4px;
        background: rgba(255, 255, 255, 0.3);
        border-radius: 2px;
        overflow: hidden;
    `;
    
    const progressBar = document.createElement('div');
    progressBar.className = 'progress-bar';
    progressBar.style.cssText = `
        width: 0%;
        height: 100%;
        background: white;
        border-radius: 2px;
        transition: width 0.3s ease;
    `;
    
    progressContainer.appendChild(progressBar);
    laptopScreen.appendChild(progressContainer);
    
    // Animar progresso
    let progress = 0;
    const progressInterval = setInterval(() => {
        progress += Math.random() * 15;
        if (progress > 100) {
            progress = 100;
            clearInterval(progressInterval);
        }
        progressBar.style.width = progress + '%';
    }, 300);
}


// Animação de entrada dos elementos
function initEntranceAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    });
    
    // Observar elementos para animação
    const elementsToAnimate = document.querySelectorAll('.main-title, .description, .cta-button, .laptop');
    elementsToAnimate.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}


// Adicionar CSS para animações dinamicamente
function addDynamicStyles() {
    const style = document.createElement('style');
    style.textContent = `
        @keyframes ripple {
            to {
                transform: scale(2);
                opacity: 0;
            }
        }
        
        .progress-container {
            animation: slideIn 0.5s ease 2s both;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(-50%) translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateX(-50%) translateY(0);
            }
        }
    `;
    document.head.appendChild(style);
}


// Função para notificação de download concluído
function showDownloadNotification() {
    // Verificar se o navegador suporta notificações
    if ('Notification' in window) {
        Notification.requestPermission().then(permission => {
            if (permission === 'granted') {
                setTimeout(() => {
                    new Notification('Download Concluído!', {
                        body: 'Seu arquivo foi baixado com sucesso.',
                        icon: '/static/images/download-icon.png'
                    });
                }, 10000);
            }
        });
    }
}

// Inicializar estilos dinâmicos
addDynamicStyles();

// Inicializar animações de entrada
initEntranceAnimations();
