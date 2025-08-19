// ===== Main JavaScript File =====

document.addEventListener('DOMContentLoaded', function () {
    // Позначити сторінку як завантажену
    document.body.classList.add('loaded');

    // Mobile menu toggle
    initMobileMenu();

    // Language switcher
    initLanguageSwitcher();

    // Smooth scrolling for anchor links
    initSmoothScrolling();

    // Form validation
    initFormValidation();

    // Lazy loading for images
    initLazyLoading();

    // Анімації при прокрутці
    initScrollAnimations();

    // Перемикання fade-in/fade-out
    initToggleAnimations();
});

// ===== Mobile Menu =====
function initMobileMenu() {
    const mobileToggle = document.querySelector('.mobile-menu-toggle');
    const headerNav = document.querySelector('.header__nav');

    if (!mobileToggle || !headerNav) {
        console.warn('Mobile menu elements not found');
        return;
    }

    mobileToggle.addEventListener('click', function () {
        headerNav.classList.toggle('is-open');
        mobileToggle.classList.toggle('is-active');

        // Toggle aria-expanded
        const isExpanded = headerNav.classList.contains('is-open');
        mobileToggle.setAttribute('aria-expanded', isExpanded);
    });

    // Close menu when clicking outside
    document.addEventListener('click', function (event) {
        if (!headerNav.contains(event.target) && !mobileToggle.contains(event.target)) {
            headerNav.classList.remove('is-open');
            mobileToggle.classList.remove('is-active');
            mobileToggle.setAttribute('aria-expanded', 'false');
        }
    });
}

// ===== Language Switcher =====
function initLanguageSwitcher() {
    const languageLinks = document.querySelectorAll('.language-switcher__link');

    if (languageLinks.length === 0) {
        console.warn('Language switcher links not found');
        return;
    }

    languageLinks.forEach(link => {
        link.addEventListener('click', function (event) {
            const language = this.dataset.language;

            // Store selected language in localStorage
            localStorage.setItem('preferred_language', language);

            // Add loading state
            this.classList.add('loading');
            this.textContent = '...';
        });
    });
}

// ===== Smooth Scrolling =====
function initSmoothScrolling() {
    const anchorLinks = document.querySelectorAll('a[href^="#"]');

    anchorLinks.forEach(link => {
        link.addEventListener('click', function (event) {
            const href = this.getAttribute('href');

            if (href === '#') return;

            const target = document.querySelector(href);
            if (target) {
                event.preventDefault();

                const headerHeight = document.querySelector('.header').offsetHeight;
                const targetPosition = target.offsetTop - headerHeight;

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// ===== Form Validation =====
function initFormValidation() {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', function (event) {
            if (!validateForm(this)) {
                event.preventDefault();
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
    const isRequired = field.hasAttribute('required');
    const type = field.type;

    // Clear previous errors
    clearFieldError(field);

    // Required field validation
    if (isRequired && !value) {
        showFieldError(field, 'Це поле обов\'язкове');
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
    const errorDiv = document.createElement('div');
    errorDiv.className = 'field-error';
    errorDiv.textContent = message;
    errorDiv.style.color = 'var(--error)';
    errorDiv.style.fontSize = 'var(--text-sm)';
    errorDiv.style.marginTop = 'var(--spacing-1)';

    field.parentNode.appendChild(errorDiv);
    field.classList.add('has-error');
}

function clearFieldError(field) {
    const errorDiv = field.parentNode.querySelector('.field-error');
    if (errorDiv) {
        errorDiv.remove();
        field.classList.remove('has-error');
    }
}

// ===== Lazy Loading =====
function initLazyLoading() {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });

        const lazyImages = document.querySelectorAll('img[data-src]');
        lazyImages.forEach(img => imageObserver.observe(img));
    }
}

// ===== Utility Functions =====

// Debounce function for performance
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

// Throttle function for scroll events
function throttle(func, limit) {
    let inThrottle;
    return function () {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

// Format phone number
function formatPhoneNumber(phone) {
    const cleaned = phone.replace(/\D/g, '');
    const match = cleaned.match(/^(\d{1})(\d{3})(\d{3})(\d{2})(\d{2})$/);
    if (match) {
        return `+${match[1]} (${match[2]}) ${match[3]}-${match[4]}-${match[5]}`;
    }
    return phone;
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification--${type}`;
    notification.textContent = message;

    // Add styles
    notification.style.position = 'fixed';
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.padding = 'var(--spacing-4)';
    notification.style.borderRadius = '8px';
    notification.style.color = 'var(--white)';
    notification.style.fontWeight = 'var(--font-medium)';
    notification.style.zIndex = '1000';
    notification.style.maxWidth = '300px';
    notification.style.boxShadow = 'var(--shadow-lg)';

    // Set background color based on type
    switch (type) {
        case 'success':
            notification.style.background = 'var(--success)';
            break;
        case 'error':
            notification.style.background = 'var(--error)';
            break;
        case 'warning':
            notification.style.background = 'var(--warning)';
            break;
        default:
            notification.style.background = 'var(--info)';
    }

    document.body.appendChild(notification);

    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 5000);

    // Click to dismiss
    notification.addEventListener('click', function () {
        if (this.parentNode) {
            this.parentNode.removeChild(this);
        }
    });
}

// ===== Performance Optimizations =====

// Optimize scroll events
const optimizedScrollHandler = throttle(function () {
    // Add scroll-based animations or effects here
    const scrolled = window.pageYOffset;
    const header = document.querySelector('.header');

    if (header) {
        if (scrolled > 100) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    }

    // Параллакс ефект для hero секції
    const heroImage = document.querySelector('.hero__image');
    if (heroImage && !shouldReduceMotion()) {
        const scrollPercent = scrolled / window.innerHeight;
        heroImage.style.transform = `translateY(${scrollPercent * 30}px)`;
    }
}, 16); // ~60fps

window.addEventListener('scroll', optimizedScrollHandler);

// Optimize resize events
const optimizedResizeHandler = debounce(function () {
    // Handle responsive behavior here
    const isMobile = window.innerWidth < 768;
    const headerNav = document.querySelector('.header__nav');

    if (headerNav) {
        if (isMobile) {
            headerNav.classList.remove('is-open');
        }
    }
}, 250);

window.addEventListener('resize', optimizedResizeHandler);

// ===== Accessibility Improvements =====

// Skip to main content link
function createSkipLink() {
    const skipLink = document.createElement('a');
    skipLink.href = '#main';
    skipLink.textContent = 'Перейти до основного контенту';
    skipLink.className = 'skip-link';

    // Add styles
    skipLink.style.position = 'absolute';
    skipLink.style.top = '-40px';
    skipLink.style.left = '6px';
    skipLink.style.background = 'var(--brand-blue)';
    skipLink.style.color = 'var(--white)';
    skipLink.style.padding = 'var(--spacing-2) var(--spacing-4)';
    skipLink.style.textDecoration = 'none';
    skipLink.style.borderRadius = '4px';
    skipLink.style.zIndex = '1001';
    skipLink.style.transition = 'top var(--transition-normal)';

    skipLink.addEventListener('focus', function () {
        this.style.top = '6px';
    });

    skipLink.addEventListener('blur', function () {
        this.style.top = '-40px';
    });

    document.body.insertBefore(skipLink, document.body.firstChild);
}

// Initialize skip link
createSkipLink();

// Add main content ID
const mainContent = document.querySelector('.main');
if (mainContent) {
    mainContent.id = 'main';
}

// ===== Анімації при прокрутці =====

function initScrollAnimations() {
    // Налаштування IntersectionObserver
    const options = {
        root: null,
        rootMargin: '0px',
        threshold: 0.5
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
                observer.unobserve(entry.target);
            }
        });
    }, options);

    // Спостерігати за елементами
    const animatedElements = document.querySelectorAll('.js-observe');
    animatedElements.forEach(el => observer.observe(el));
}

// ===== Перемикання анімацій =====

function initToggleAnimations() {
    const toggleElements = document.querySelectorAll('.toggle-target');

    toggleElements.forEach(elem => {
        elem.addEventListener('click', function () {
            if (this.classList.contains('fade-in')) {
                this.classList.replace('fade-in', 'fade-out');
            } else {
                this.classList.replace('fade-out', 'fade-in');
            }
        });
    });
}

// ===== Допоміжні функції для анімацій =====

// Додати клас анімації до елемента
function addAnimationClass(element, animationClass) {
    if (element && !element.classList.contains(animationClass)) {
        element.classList.add(animationClass);
    }
}

// Установити затримку для анімацій
function setAnimationDelay(element, delay) {
    if (element) {
        element.style.animationDelay = delay + 'ms';
    }
}

// Анімація списку елементів з затримкою
function animateListWithDelay(selector, animationClass, delayStep = 100) {
    const elements = document.querySelectorAll(selector);
    elements.forEach((element, index) => {
        setTimeout(() => {
            addAnimationClass(element, animationClass);
        }, index * delayStep);
    });
}

// Перевірка на prefers-reduced-motion
function shouldReduceMotion() {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

// Пульсація кнопки при кліку
function addPulseEffect(buttonSelector) {
    const buttons = document.querySelectorAll(buttonSelector);

    buttons.forEach(button => {
        button.addEventListener('click', function (e) {
            if (shouldReduceMotion()) return;

            this.classList.add('pulse');

            setTimeout(() => {
                this.classList.remove('pulse');
            }, 600);
        });
    });
}

// Ініціалізація ефектів
setTimeout(() => {
    addPulseEffect('.btn--primary');

    // Анімація карток з затримкою
    if (!shouldReduceMotion()) {
        animateListWithDelay('.card', 'fade-in', 150);
        animateListWithDelay('.equipment-card', 'slide-in-up', 100);
    }
}, 500);
