/* ===== ADIABATIC JAVASCRIPT - CLEAN & MOBILE OPTIMIZED ===== */

document.addEventListener('DOMContentLoaded', function () {
    // Initialize all components
    initMobileMenu();
    initSmoothScrolling();
    initFormValidation();
    initIOSFixes();
    initDesktopAnimatedMenu();

    console.log('🚀 Adiabatic JavaScript loaded successfully!');
});

/* ===== MOBILE MENU ===== */
function initMobileMenu() {
    const toggle = document.querySelector('.mobile-toggle');
    const menu = document.querySelector('.mobile-menu');
    const navLinks = document.querySelectorAll('.mobile-nav-link');

    if (!toggle || !menu) return;

    // Toggle menu
    toggle.addEventListener('click', function (e) {
        e.preventDefault();
        const isOpen = menu.classList.contains('open');

        if (isOpen) {
            closeMenu();
        } else {
            openMenu();
        }
    });

    // Close menu when clicking nav links
    navLinks.forEach(link => {
        link.addEventListener('click', function () {
            if (window.innerWidth < 768) {
                closeMenu();
            }
        });
    });

    // Close menu when clicking outside
    document.addEventListener('click', function (e) {
        if (!toggle.contains(e.target) && !menu.contains(e.target)) {
            closeMenu();
        }
    });

    // Close menu on escape
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
            closeMenu();
        }
    });

    // Close menu on orientation change
    window.addEventListener('orientationchange', function () {
        setTimeout(closeMenu, 100);
    });

    function openMenu() {
        menu.classList.add('open');
        toggle.classList.add('active');
        document.body.style.overflow = 'hidden';
        toggle.setAttribute('aria-expanded', 'true');

        // Focus first menu item for accessibility
        const firstLink = menu.querySelector('.mobile-nav-link');
        if (firstLink) {
            setTimeout(() => firstLink.focus(), 100);
        }
    }

    function closeMenu() {
        menu.classList.remove('open');
        toggle.classList.remove('active');
        document.body.style.overflow = '';
        toggle.setAttribute('aria-expanded', 'false');
    }
}

/* ===== SMOOTH SCROLLING ===== */
function initSmoothScrolling() {
    const anchors = document.querySelectorAll('a[href^="#"]');

    anchors.forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href === '#' || !href) return;

            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();

                const headerHeight = document.querySelector('.header')?.offsetHeight || 0;
                const targetPosition = target.offsetTop - headerHeight - 20;

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

/* ===== FORM VALIDATION ===== */
function initFormValidation() {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', function (e) {
            if (!validateForm(this)) {
                e.preventDefault();
            }
        });

        // Real-time validation
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('blur', function () {
                validateField(this);
            });

            input.addEventListener('input', function () {
                clearFieldError(this);
            });
        });
    });
}

function validateForm(form) {
    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');

    requiredFields.forEach(field => {
        if (!validateField(field)) {
            isValid = false;
        }
    });

    return isValid;
}

function validateField(field) {
    const value = field.value.trim();
    const type = field.type;
    const isRequired = field.hasAttribute('required');

    clearFieldError(field);

    // Required validation
    if (isRequired && !value) {
        showFieldError(field, "Це поле обов'язкове");
        return false;
    }

    // Email validation
    if (type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            showFieldError(field, 'Введіть коректний email');
            return false;
        }
    }

    // Phone validation
    if (type === 'tel' && value) {
        const phoneRegex = /^[\+]?[0-9\s\-\(\)]{10,}$/;
        if (!phoneRegex.test(value)) {
            showFieldError(field, 'Введіть коректний номер телефону');
            return false;
        }
    }

    return true;
}

function showFieldError(field, message) {
    const error = document.createElement('div');
    error.className = 'field-error';
    error.textContent = message;
    error.style.cssText = `
        color: #dc2626;
        font-size: 0.875rem;
        margin-top: 0.25rem;
    `;

    field.parentNode.appendChild(error);
    field.classList.add('error');
}

function clearFieldError(field) {
    const error = field.parentNode.querySelector('.field-error');
    if (error) {
        error.remove();
    }
    field.classList.remove('error');
}

/* ===== iOS FIXES ===== */
function initIOSFixes() {
    const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent);

    if (isIOS) {
        document.body.classList.add('ios');

        // Fix viewport height
        function setViewportHeight() {
            const vh = window.innerHeight * 0.01;
            document.documentElement.style.setProperty('--vh', `${vh}px`);
        }

        setViewportHeight();
        window.addEventListener('resize', debounce(setViewportHeight, 100));
        window.addEventListener('orientationchange', debounce(setViewportHeight, 100));

        // Prevent zoom on input focus
        const inputs = document.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('focus', function () {
                const viewport = document.querySelector('meta[name=viewport]');
                if (viewport) {
                    const originalContent = viewport.content;
                    viewport.content = 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no';

                    this.addEventListener('blur', function () {
                        setTimeout(() => {
                            viewport.content = originalContent;
                        }, 100);
                    }, { once: true });
                }
            });
        });
    }
}

/* ===== UTILITY FUNCTIONS ===== */
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

/* ===== DOWNLOAD TRACKING ===== */
function trackDownload(filename) {
    // Analytics tracking for downloads
    if (typeof gtag !== 'undefined') {
        gtag('event', 'download', {
            event_category: 'engagement',
            event_label: filename
        });
    }

    console.log('Download tracked:', filename);
}

// Add download tracking to download links
document.addEventListener('DOMContentLoaded', function () {
    const downloadLinks = document.querySelectorAll('.download-link, [href*=".pdf"], [href*=".doc"], [href*=".xls"]');

    downloadLinks.forEach(link => {
        link.addEventListener('click', function () {
            const filename = this.getAttribute('href').split('/').pop() || this.textContent.trim();
            trackDownload(filename);
        });
    });
});

/* ===== ERROR HANDLING ===== */
window.addEventListener('error', function (e) {
    console.error('JavaScript Error:', e.error);
});

window.addEventListener('unhandledrejection', function (e) {
    console.error('Unhandled Promise Rejection:', e.reason);
});

/* ===== INTERSECTION OBSERVER FOR ANIMATIONS ===== */
if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
                observer.unobserve(entry.target);
            }
        });
    }, {
        rootMargin: '0px 0px -50px 0px',
        threshold: 0.1
    });

    // Observe elements for animation
    document.addEventListener('DOMContentLoaded', function () {
        const animatedElements = document.querySelectorAll('.card, .section-header');
        animatedElements.forEach(el => {
            observer.observe(el);
        });
    });
}

/* ===== PERFORMANCE MONITORING ===== */
if ('performance' in window) {
    window.addEventListener('load', function () {
        setTimeout(() => {
            const perfData = performance.getEntriesByType('navigation')[0];
            console.log('Page Load Time:', Math.round(perfData.loadEventEnd - perfData.fetchStart), 'ms');
        }, 0);
    });
}

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

/* ===== DESKTOP ANIMATED MENU ===== */

class AnimatedDesktopMenu {
    constructor() {
        this.isMenuOpen = false;
        this.isAnimating = false;
        this.isMobile = window.innerWidth < 768;

        this.burger = document.querySelector('.desktop-burger-btn');
        this.logo = document.querySelector('.logo');
        this.menu = document.querySelector('.animated-desktop-menu');

        this.init();
    }

    init() {
        console.log('🔧 AnimatedDesktopMenu.init() called');
        console.log('Elements found:', {
            burger: !!this.burger,
            logo: !!this.logo,
            menu: !!this.menu
        });
        console.log('Is mobile?', this.isMobile);

        if (!this.burger || !this.logo || !this.menu) {
            console.error('❌ Missing required elements for desktop menu');
            return;
        }

        // Only initialize on desktop
        if (this.isMobile) {
            console.log('📱 Mobile detected, not initializing desktop menu');
            return;
        }

        this.setupEventListeners();
        this.setupResponsive();
        console.log('✅ Desktop Animated Menu initialized successfully');
    }

    setupEventListeners() {
        // Burger button click
        this.burger.addEventListener('click', (e) => {
            e.preventDefault();
            this.handleBurgerClick();
        });

        // Close menu when clicking menu links
        const menuLinks = this.menu.querySelectorAll('.animated-nav-link');
        menuLinks.forEach(link => {
            link.addEventListener('click', () => {
                this.closeMenu();
            });
        });

        // Close menu on Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isMenuOpen) {
                this.closeMenu();
            }
        });
    }

    setupResponsive() {
        // Handle window resize
        window.addEventListener('resize', debounce(() => {
            const newIsMobile = window.innerWidth < 768;

            if (newIsMobile !== this.isMobile) {
                this.isMobile = newIsMobile;

                // Close menu if switching to mobile
                if (this.isMobile && this.isMenuOpen) {
                    this.closeMenu(true); // Force close without animation
                }
            }
        }, 250));
    }

    handleBurgerClick() {
        if (this.isAnimating) return;

        if (this.isMenuOpen) {
            this.closeMenu();
        } else {
            this.openMenu();
        }
    }

    openMenu() {
        if (this.isAnimating || this.isMenuOpen || this.isMobile) return;

        this.isAnimating = true;
        this.isMenuOpen = true;

        // Update burger button
        this.burger.classList.add('active');
        this.burger.setAttribute('aria-expanded', 'true');

        // Start logo animation (moving LEFT from right position)
        this.logo.classList.add('moving-left');

        // Show menu after logo starts moving
        setTimeout(() => {
            this.menu.classList.add('active');
        }, 200);

        // Animation complete
        setTimeout(() => {
            this.isAnimating = false;
        }, 1000);

        console.log('📤 Desktop menu opened');
    }

    closeMenu(force = false) {
        if (!force && (this.isAnimating || !this.isMenuOpen)) return;

        this.isAnimating = true;
        this.isMenuOpen = false;

        // Hide menu first
        this.menu.classList.remove('active');

        // Start logo return animation (moving RIGHT back to original position)
        setTimeout(() => {
            this.logo.classList.remove('moving-left');
            this.logo.classList.add('moving-right');
        }, 100);

        // Reset burger button
        setTimeout(() => {
            this.burger.classList.remove('active');
            this.burger.setAttribute('aria-expanded', 'false');
        }, 300);

        // Clean up logo classes
        setTimeout(() => {
            this.logo.classList.remove('moving-right');
            this.isAnimating = false;
        }, 700);

        console.log('📥 Desktop menu closed');
    }

    // Public methods for external access
    isOpen() {
        return this.isMenuOpen;
    }

    toggle() {
        this.handleBurgerClick();
    }
}

/* ===== INIT DESKTOP ANIMATED MENU ===== */
function initDesktopAnimatedMenu() {
    console.log('🔍 Checking desktop menu initialization...');
    console.log('Window width:', window.innerWidth);
    console.log('Is desktop?', window.innerWidth >= 768);

    // Only initialize on desktop
    if (window.innerWidth >= 768) {
        console.log('🎯 Initializing desktop animated menu...');
        window.animatedDesktopMenu = new AnimatedDesktopMenu();
    } else {
        console.log('📱 Mobile detected, skipping desktop menu');
    }
}

// Initialize 3D Gallery when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.gallery3D = new Gallery3D();
});

/* ===== FIXED VIDEO BACKGROUND EFFECT ===== */
document.addEventListener('DOMContentLoaded', function () {
    console.log('🎯 Initializing fixed video background...');

    // Ensure sections stack properly over video
    const sections = document.querySelectorAll('.section:not(.hero)');
    sections.forEach((section, index) => {
        section.style.position = 'relative';
        section.style.zIndex = 10 + index;
        section.style.background = section.style.background || 'var(--white)';
    });

    // Header transparency effect on scroll
    const header = document.querySelector('.header');
    if (header) {
        window.addEventListener('scroll', function () {
            const scrolled = window.pageYOffset;
            if (scrolled > 100) {
                header.style.background = 'rgba(27, 54, 93, 0.95)';
                header.style.backdropFilter = 'blur(10px)';
            } else {
                header.style.background = 'var(--primary)';
                header.style.backdropFilter = 'none';
            }
        }, { passive: true });
    }

    // Video optimization for mobile
    const heroVideo = document.querySelector('.hero-video');
    const isTouch = 'ontouchstart' in window;
    const isMobile = window.innerWidth <= 768;

    if (heroVideo) {
        if (isTouch || isMobile) {
            // Pause video on mobile to save battery
            heroVideo.pause();
            heroVideo.style.opacity = '0.8';
            console.log('📱 Video paused on mobile device');
        } else {
            console.log('🎬 Video playing on desktop');
        }
    }

    console.log('✅ Fixed video background initialized');
});