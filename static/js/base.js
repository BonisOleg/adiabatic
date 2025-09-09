/* ===== ADIABATIC BASE JAVASCRIPT ===== */

document.addEventListener('DOMContentLoaded', function () {
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

/* ===== BACK TO TOP BUTTON ===== */
function initBackToTop() {
    const backToTopBtn = document.querySelector('.back-to-top');
    if (!backToTopBtn) return;

    window.addEventListener('scroll', function () {
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

/* ===== ERROR HANDLING ===== */
window.addEventListener('error', function (e) {
    console.error('JavaScript Error:', e.error);
});

window.addEventListener('unhandledrejection', function (e) {
    console.error('Unhandled Promise Rejection:', e.reason);
});

/* ===== PERFORMANCE MONITORING ===== */
if ('performance' in window) {
    window.addEventListener('load', function () {
        setTimeout(() => {
            const perfData = performance.getEntriesByType('navigation')[0];
            console.log('Page Load Time:', Math.round(perfData.loadEventEnd - perfData.fetchStart), 'ms');
        }, 0);
    });
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
