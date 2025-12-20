/* ===== ADIABATIC BASE JAVASCRIPT ===== */
/* global gtag */

import { debounce } from './utils.js';

document.addEventListener('DOMContentLoaded', () => {
    // Initialize base components
    initMobileMenu();
    initSmoothScrolling();
    initIOSFixes();
    initBackToTop();
    initIntersectionObserver();

    console.log('🚀 Adiabatic Base JavaScript loaded successfully!');
});

/* ===== MOBILE MENU ===== */
function initMobileMenu() {
    const logoLink = document.querySelector('.mobile-menu-trigger');
    const menu = document.querySelector('.mobile-menu');
    const navLinks = document.querySelectorAll('.mobile-nav-link');

    if (!logoLink || !menu) return;

    // Toggle menu when clicking logo
    logoLink.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        const isOpen = menu.classList.contains('open');

        if (isOpen) {
            closeMenu();
        } else {
            openMenu();
        }
    });

    // Close menu when clicking the close button (::before pseudo-element)
    menu.addEventListener('click', (e) => {
        // Check if click is in the close button area (top-right)
        const rect = menu.getBoundingClientRect();
        const clickX = e.clientX - rect.left;
        const clickY = e.clientY - rect.top;

        // Close button area (top-right corner, approximately)
        if (clickX > rect.width - 80 && clickY < 80) {
            e.preventDefault();
            closeMenu();
        }
    });

    // Close menu when clicking nav links
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (window.innerWidth < 768) {
                setTimeout(closeMenu, 200); // Small delay for better UX
            }
        });
    });

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
        if (!logoLink.contains(e.target) && !menu.contains(e.target)) {
            closeMenu();
        }
    });

    // Close menu on escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && menu.classList.contains('open')) {
            closeMenu();
        }
    });

    // Close menu on orientation change
    window.addEventListener('orientationchange', () => {
        setTimeout(closeMenu, 300);
    });

    // Handle swipe gestures for iOS
    let touchStartX = 0;
    let touchStartY = 0;

    menu.addEventListener('touchstart', (e) => {
        touchStartX = e.touches[0].clientX;
        touchStartY = e.touches[0].clientY;
    }, { passive: true });

    menu.addEventListener('touchend', (e) => {
        const touchEndX = e.changedTouches[0].clientX;
        const touchEndY = e.changedTouches[0].clientY;
        const deltaX = touchEndX - touchStartX;
        const deltaY = touchEndY - touchStartY;

        // Swipe left to close (threshold: 50px)
        if (deltaX < -50 && Math.abs(deltaY) < 100) {
            closeMenu();
        }
    }, { passive: true });

    function openMenu() {
        menu.classList.add('open');
        logoLink.classList.add('active');
        logoLink.setAttribute('aria-expanded', 'true');

        // Prevent body scroll with iOS support
        document.body.style.overflow = 'hidden';
        document.body.style.position = 'fixed';
        document.body.style.width = '100%';

        // iOS Safari viewport fix
        if (/iPad|iPhone|iPod/.test(navigator.userAgent)) {
            document.body.style.height = '100vh';
            document.body.style.webkitOverflowScrolling = 'touch';
        }

        // Focus first menu item for accessibility
        const firstLink = menu.querySelector('.mobile-nav-link');
        if (firstLink) {
            setTimeout(() => firstLink.focus(), 200);
        }

        console.log('📱 Мобільне меню відкрито');
    }

    function closeMenu() {
        menu.classList.remove('open');
        logoLink.classList.remove('active');
        logoLink.setAttribute('aria-expanded', 'false');

        // Restore body scroll
        document.body.style.overflow = '';
        document.body.style.position = '';
        document.body.style.width = '';
        document.body.style.height = '';
        document.body.style.webkitOverflowScrolling = '';

        console.log('📱 Мобільне меню закрито');
    }

    // Добавити візуальний фідбек для натискань
    logoLink.addEventListener('touchstart', function () {
        this.style.transform = 'scale(0.95)';
    }, { passive: true });

    logoLink.addEventListener('touchend', function () {
        this.style.transform = '';
    }, { passive: true });

    console.log('🔧 Мобільне меню ініціалізовано успішно');
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

/* ===== BACK TO TOP BUTTON ===== */
function initBackToTop() {
    const backToTopBtn = document.querySelector('.back-to-top') || document.getElementById('backToTop');
    if (!backToTopBtn) return;

    // Scroll handler
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            backToTopBtn.classList.add('visible');
            backToTopBtn.style.opacity = '1';
            backToTopBtn.style.visibility = 'visible';
        } else {
            backToTopBtn.classList.remove('visible');
            backToTopBtn.style.opacity = '0';
            backToTopBtn.style.visibility = 'hidden';
        }
    }, { passive: true });

    // Click handler
    backToTopBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

/* ===== iOS FIXES ===== */
function initIOSFixes() {
    const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent);

    if (isIOS) {
        document.body.classList.add('ios');

        // Fix viewport height
        const setViewportHeight = () => {
            const vh = window.innerHeight * 0.01;
            document.documentElement.style.setProperty('--vh', `${vh}px`);
        };

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

                    this.addEventListener('blur', () => {
                        setTimeout(() => {
                            viewport.content = originalContent;
                        }, 100);
                    }, { once: true });
                }
            });
        });
    }
}

/* ===== INTERSECTION OBSERVER FOR ANIMATIONS ===== */
function initIntersectionObserver() {
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
        const animatedElements = document.querySelectorAll('.card, .section-header, .js-observe');
        animatedElements.forEach(el => {
            observer.observe(el);
        });
    }
}

/* ===== UTILITY FUNCTIONS ===== */
window.debounce = function (func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
};

/* ===== ERROR HANDLING ===== */
window.addEventListener('error', (e) => {
    console.error('JavaScript Error:', e.error);
});

window.addEventListener('unhandledrejection', (e) => {
    console.error('Unhandled Promise Rejection:', e.reason);
});

/* ===== PERFORMANCE MONITORING ===== */
if ('performance' in window) {
    window.addEventListener('load', () => {
        setTimeout(() => {
            const perfData = performance.getEntriesByType('navigation')[0];
            console.log('Page Load Time:', Math.round(perfData.loadEventEnd - perfData.fetchStart), 'ms');
        }, 0);
    });
}

/* ===== BFCACHE SUPPORT (Safari/Firefox) ===== */
window.addEventListener('pageshow', (event) => {
    if (event.persisted) {
        console.log('📄 Page restored from bfcache');
        
        // Оновити динамічний контент
        const forms = document.querySelectorAll('form');
        forms.forEach(form => form.reset());
        
        // Trigger HTMX reload якщо є динамічний контент
        if (typeof htmx !== 'undefined') {
            htmx.trigger(document.body, 'pageRestored');
        }
        
        // Оновити timestamp елементи якщо є
        const timestamps = document.querySelectorAll('[data-timestamp]');
        timestamps.forEach(el => {
            const time = parseInt(el.dataset.timestamp);
            if (time) {
                el.textContent = formatRelativeTime(time);
            }
        });
    }
});

// Helper для форматування часу
function formatRelativeTime(timestamp) {
    const seconds = Math.floor((Date.now() - timestamp) / 1000);
    if (seconds < 60) return 'щойно';
    if (seconds < 3600) return `${Math.floor(seconds / 60)} хв тому`;
    if (seconds < 86400) return `${Math.floor(seconds / 3600)} год тому`;
    return `${Math.floor(seconds / 86400)} дн тому`;
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
document.addEventListener('DOMContentLoaded', () => {
    const downloadLinks = document.querySelectorAll('.download-link, [href*=".pdf"], [href*=".doc"], [href*=".xls"]');

    downloadLinks.forEach(link => {
        link.addEventListener('click', function () {
            // Перевіряємо data-download атрибут спочатку
            const dataDownload = this.getAttribute('data-download');
            const filename = dataDownload || this.getAttribute('href').split('/').pop() || this.textContent.trim();
            trackDownload(filename);
        });
    });
});
