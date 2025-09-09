/* ===== 3D GALLERY FUNCTIONALITY ===== */

class Gallery3D {
    constructor() {
        this.currentModal = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.detectMobile();
        console.log('🧊 3D Gallery initialized');
    }

    detectMobile() {
        this.isMobile = window.innerWidth <= 768 || /Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
        this.isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent);

        // iOS Safari specific optimizations
        if (this.isIOS) {
            document.body.classList.add('ios-safari');
            this.setupIOSOptimizations();
        }
    }

    setupIOSOptimizations() {
        // Prevent zoom on double tap
        let lastTouchEnd = 0;
        document.addEventListener('touchend', function (event) {
            const now = (new Date()).getTime();
            if (now - lastTouchEnd <= 300) {
                event.preventDefault();
            }
            lastTouchEnd = now;
        }, false);

        // Fix viewport height for modals
        function setVH() {
            let vh = window.innerHeight * 0.01;
            document.documentElement.style.setProperty('--vh', `${vh}px`);
        }
        setVH();
        window.addEventListener('resize', setVH);
        window.addEventListener('orientationchange', () => {
            setTimeout(setVH, 100);
        });
    }

    setupEventListeners() {
        // 3D viewer buttons
        document.addEventListener('click', (e) => {
            if (e.target.closest('.btn--3d')) {
                e.preventDefault();
                this.handle3DButton(e.target.closest('.btn--3d'));
            }

            if (e.target.closest('.viewer-3d-close')) {
                this.closeModal();
            }

            if (e.target.closest('.viewer-3d-control')) {
                this.handle3DControl(e.target.closest('.viewer-3d-control'));
            }
        });

        // Modal background click
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('viewer-3d-modal')) {
                this.closeModal();
            }
        });

        // Keyboard controls
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeModal();
            }
        });
    }

    handle3DButton(button) {
        const file3D = button.dataset['3dFile'];
        const title = button.dataset.title;
        const productId = button.dataset.productId;

        if (!file3D) {
            this.showNotification('3D файл недоступний', 'warning');
            return;
        }

        // Check file extension
        const extension = file3D.split('.').pop().toLowerCase();
        const supportedFormats = ['gltf', 'glb', 'obj'];

        if (supportedFormats.includes(extension)) {
            this.open3DViewer(file3D, title, productId);
        } else {
            // Fallback for CAD files - offer download
            this.showCADFileModal(file3D, title);
        }
    }

    open3DViewer(file3D, title, productId) {
        // Create modal if it doesn't exist
        if (!document.getElementById('viewer3DModal')) {
            this.create3DModal();
        }

        const modal = document.getElementById('viewer3DModal');
        const titleElement = modal.querySelector('.viewer-3d-title');
        const loading = modal.querySelector('.viewer-3d-loading');

        // Set title
        if (titleElement) titleElement.textContent = title;

        // Show modal
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
        this.currentModal = modal;

        // Show loading
        if (loading) loading.style.display = 'block';

        // For now, show a message that 3D viewer is being loaded
        setTimeout(() => {
            if (loading) loading.innerHTML = `
                <div class="loading-spinner"></div>
                <p>3D переглядач завантажується...</p>
                <p><small>Для повної функціональності потрібна інтеграція Three.js</small></p>
                <button class="btn btn--secondary btn--small" onclick="window.open('${file3D}', '_blank')">
                    📥 Завантажити файл
                </button>
            `;
        }, 1000);
    }

    showCADFileModal(file3D, title) {
        const extension = file3D.split('.').pop().toUpperCase();

        const modal = document.createElement('div');
        modal.className = 'viewer-3d-modal active';
        modal.innerHTML = `
            <div class="viewer-3d-container" style="max-width: 500px; height: auto;">
                <div class="viewer-3d-header">
                    <h3 class="viewer-3d-title">${title}</h3>
                    <button class="viewer-3d-close">&times;</button>
                </div>
                <div class="viewer-3d-content" style="padding: var(--space-6); text-align: center;">
                    <div class="cad-file-info">
                        <div class="file-icon" style="font-size: 4rem; margin-bottom: var(--space-4);">📐</div>
                        <h4>CAD файл ${extension}</h4>
                        <p style="margin: var(--space-4) 0; color: var(--gray-600);">
                            Це професійний CAD файл. Для перегляду рекомендуємо використовувати 
                            спеціалізоване ПЗ або CAD переглядач.
                        </p>
                        <div style="display: flex; gap: var(--space-3); justify-content: center; flex-wrap: wrap;">
                            <a href="${file3D}" download class="btn btn--primary">
                                📥 Завантажити файл
                            </a>
                            <button class="btn btn--secondary viewer-3d-close">
                                Закрити
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
        document.body.style.overflow = 'hidden';
        this.currentModal = modal;

        // Auto-remove after closing
        modal.addEventListener('click', (e) => {
            if (e.target === modal || e.target.classList.contains('viewer-3d-close')) {
                modal.remove();
                document.body.style.overflow = '';
                this.currentModal = null;
            }
        });
    }

    create3DModal() {
        const modal = document.createElement('div');
        modal.id = 'viewer3DModal';
        modal.className = 'viewer-3d-modal';
        modal.innerHTML = `
            <div class="viewer-3d-container">
                <div class="viewer-3d-header">
                    <h3 class="viewer-3d-title">3D Модель</h3>
                    <button class="viewer-3d-close">&times;</button>
                </div>
                <div class="viewer-3d-content">
                    <canvas id="viewer3DCanvas"></canvas>
                    <div class="viewer-3d-loading">
                        <div class="loading-spinner"></div>
                        <p>Завантаження 3D моделі...</p>
                    </div>
                </div>
                <div class="viewer-3d-controls">
                    <button class="viewer-3d-control" data-action="reset">🔄 Скинути</button>
                    <button class="viewer-3d-control" data-action="fullscreen">📺 Повний екран</button>
                    <button class="viewer-3d-control" data-action="info">ℹ️ Інформація</button>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
    }

    handle3DControl(button) {
        const action = button.dataset.action;

        switch (action) {
            case 'reset':
                this.showNotification('Позицію скинуто', 'success');
                break;

            case 'fullscreen':
                const canvas = document.getElementById('viewer3DCanvas');
                if (canvas && canvas.requestFullscreen) {
                    canvas.requestFullscreen();
                } else {
                    this.showNotification('Повноекранний режим недоступний', 'warning');
                }
                break;

            case 'info':
                this.showNotification('3D переглядач - версія 1.0', 'info');
                break;
        }
    }

    closeModal() {
        if (this.currentModal) {
            this.currentModal.classList.remove('active');
            document.body.style.overflow = '';

            // Clean up if it's a temporary modal
            if (!this.currentModal.id) {
                setTimeout(() => {
                    if (this.currentModal && this.currentModal.parentNode) {
                        this.currentModal.remove();
                    }
                }, 300);
            }

            this.currentModal = null;
        }
    }

    showNotification(message, type = 'info') {
        // Create notification
        const notification = document.createElement('div');
        notification.className = `notification notification--${type}`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--primary);
            color: var(--white);
            padding: var(--space-3) var(--space-4);
            border-radius: var(--radius);
            box-shadow: var(--shadow-lg);
            z-index: 1001;
            max-width: 300px;
            transform: translateX(100%);
            transition: transform 0.3s ease;
        `;

        // Set color based on type
        if (type === 'success') {
            notification.style.background = '#10b981';
        } else if (type === 'warning') {
            notification.style.background = '#f59e0b';
        } else if (type === 'error') {
            notification.style.background = '#ef4444';
        }

        notification.textContent = message;
        document.body.appendChild(notification);

        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);

        // Auto remove
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 300);
        }, 3000);
    }
}

// Image modal function
function openImageModal(imageSrc, title) {
    // Remove existing image modal
    const existingModal = document.getElementById('imageModal');
    if (existingModal) {
        existingModal.remove();
    }

    const modal = document.createElement('div');
    modal.id = 'imageModal';
    modal.className = 'viewer-3d-modal active';
    modal.innerHTML = `
        <div class="viewer-3d-container">
            <div class="viewer-3d-header">
                <h3 class="viewer-3d-title">${title}</h3>
                <button class="viewer-3d-close">&times;</button>
            </div>
            <div class="viewer-3d-content" style="padding: var(--space-4);">
                <img src="${imageSrc}" 
                     style="max-width: 100%; max-height: 100%; object-fit: contain; display: block; margin: 0 auto;" 
                     alt="${title}"
                     loading="lazy">
            </div>
        </div>
    `;

    document.body.appendChild(modal);
    document.body.style.overflow = 'hidden';

    // Close handlers
    modal.addEventListener('click', (e) => {
        if (e.target === modal || e.target.classList.contains('viewer-3d-close')) {
            modal.remove();
            document.body.style.overflow = '';
        }
    });

    // Keyboard close
    const keyHandler = (e) => {
        if (e.key === 'Escape') {
            modal.remove();
            document.body.style.overflow = '';
            document.removeEventListener('keydown', keyHandler);
        }
    };
    document.addEventListener('keydown', keyHandler);
}

// Initialize 3D Gallery when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.gallery3D = new Gallery3D();
});
