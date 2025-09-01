/* ===== ADIABATIC JAVASCRIPT - CLEAN & MOBILE OPTIMIZED ===== */

document.addEventListener('DOMContentLoaded', function () {
    // Initialize all components
    initMobileMenu();
    initSmoothScrolling();
    initFormValidation();
    initIOSFixes();

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