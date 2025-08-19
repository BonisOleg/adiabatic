/* ===== PROMSTEEL STYLE JAVASCRIPT ===== */

document.addEventListener('DOMContentLoaded', function () {
    // Позначити сторінку як завантажену
    document.body.classList.add('loaded');

    // Ініціалізація всіх компонентів
    initMobileMenu();
    initScrollAnimations();
    initHeroParallax();
    initButtonEffects();
    initSmoothScrolling();
    initUpButton();
    initHeaderScroll();
    initStaggeredAnimations();
    initLazyLoading();
    initFormValidation();

    console.log('🚀 Promsteel Style JavaScript ініціалізовано!');
});

/* ===== MOBILE MENU (Promsteel Style) ===== */
function initMobileMenu() {
    const toggle = document.querySelector('.mobile-menu-toggle');
    const nav = document.querySelector('.header__nav');

    if (!toggle || !nav) return;

    toggle.addEventListener('click', function () {
        const isOpen = nav.classList.contains('mobile-open');

        if (isOpen) {
            nav.classList.remove('mobile-open');
            toggle.classList.remove('active');
            document.body.classList.remove('menu-open');
        } else {
            nav.classList.add('mobile-open');
            toggle.classList.add('active');
            document.body.classList.add('menu-open');
        }
    });

    // Закрити меню при кліку поза ним
    document.addEventListener('click', function (e) {
        if (!toggle.contains(e.target) && !nav.contains(e.target)) {
            nav.classList.remove('mobile-open');
            toggle.classList.remove('active');
            document.body.classList.remove('menu-open');
        }
    });
}

/* ===== SCROLL ANIMATIONS (IntersectionObserver) ===== */
function initScrollAnimations() {
    if (!shouldReduceMotion()) {
        const observerOptions = {
            root: null,
            rootMargin: '0px',
            threshold: 0.1
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate');

                    // Додавання специфічних анімацій
                    const animationClass = entry.target.getAttribute('data-animation');
                    if (animationClass) {
                        entry.target.classList.add(animationClass);
                    }

                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        // Спостерігаємо за всіма елементами з класом js-observe
        const animatedElements = document.querySelectorAll('.js-observe');
        animatedElements.forEach(el => {
            observer.observe(el);

            // Додавання анімаційних класів на основі позиції
            if (el.classList.contains('slide-in-left')) {
                el.style.opacity = '0';
                el.style.transform = 'translateX(-50px)';
            } else if (el.classList.contains('slide-in-up')) {
                el.style.opacity = '0';
                el.style.transform = 'translateY(50px)';
            } else if (el.classList.contains('fade-in')) {
                el.style.opacity = '0';
                el.style.transform = 'translateY(20px)';
            }
        });
    }
}

/* ===== HERO PARALLAX EFFECT ===== */
function initHeroParallax() {
    if (shouldReduceMotion()) return;

    const heroSection = document.querySelector('.hero');
    if (!heroSection) return;

    function updateParallax() {
        const scrolled = window.pageYOffset;
        const parallaxSpeed = 0.5;
        const yPos = -(scrolled * parallaxSpeed);

        heroSection.style.transform = `translateY(${yPos}px)`;
    }

    // Throttle функція для оптимізації
    let ticking = false;
    function requestTick() {
        if (!ticking) {
            requestAnimationFrame(updateParallax);
            ticking = true;
            setTimeout(() => ticking = false, 16);
        }
    }

    window.addEventListener('scroll', requestTick);
}

/* ===== BUTTON EFFECTS (Promsteel Style) ===== */
function initButtonEffects() {
    const buttons = document.querySelectorAll('.btn');

    buttons.forEach(button => {
        // Ripple effect при кліку
        button.addEventListener('click', function (e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;

            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');

            // CSS для ripple ефекту
            ripple.style.position = 'absolute';
            ripple.style.borderRadius = '50%';
            ripple.style.background = 'rgba(255, 255, 255, 0.6)';
            ripple.style.pointerEvents = 'none';
            ripple.style.animation = 'ripple-animation 0.6s linear';

            this.appendChild(ripple);

            setTimeout(() => {
                ripple.remove();
            }, 600);
        });

        // Pulse ефект для primary кнопок
        if (button.classList.contains('btn--primary')) {
            button.addEventListener('mouseenter', function () {
                if (!shouldReduceMotion()) {
                    this.classList.add('pulse');
                    setTimeout(() => this.classList.remove('pulse'), 600);
                }
            });
        }
    });

    // Додавання CSS для ripple анімації
    if (!document.getElementById('ripple-style')) {
        const style = document.createElement('style');
        style.id = 'ripple-style';
        style.textContent = `
            @keyframes ripple-animation {
                to {
                    transform: scale(4);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }
}

/* ===== SMOOTH SCROLLING ===== */
function initSmoothScrolling() {
    const anchors = document.querySelectorAll('a[href^="#"]');

    anchors.forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
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

/* ===== UP BUTTON FUNCTIONALITY ===== */
function initUpButton() {
    const upButton = document.querySelector('.footer__up-button');
    if (!upButton) return;

    // Показувати/ховати кнопку при скролі
    function toggleUpButton() {
        if (window.pageYOffset > 300) {
            upButton.style.opacity = '1';
            upButton.style.visibility = 'visible';
            upButton.style.transform = 'translateY(0)';
        } else {
            upButton.style.opacity = '0';
            upButton.style.visibility = 'hidden';
            upButton.style.transform = 'translateY(10px)';
        }
    }

    // Ініціальні стилі
    upButton.style.transition = 'all 0.3s ease';
    upButton.style.opacity = '0';
    upButton.style.visibility = 'hidden';
    upButton.style.transform = 'translateY(10px)';

    // Throttle для оптимізації
    let ticking = false;
    function requestTick() {
        if (!ticking) {
            requestAnimationFrame(toggleUpButton);
            ticking = true;
            setTimeout(() => ticking = false, 16);
        }
    }

    window.addEventListener('scroll', requestTick);
}

/* ===== HEADER SCROLL EFFECT ===== */
function initHeaderScroll() {
    const header = document.querySelector('.header');
    if (!header) return;

    let lastScrollTop = 0;

    function handleHeaderScroll() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

        if (scrollTop > 100) {
            header.classList.add('header--scrolled');
        } else {
            header.classList.remove('header--scrolled');
        }

        // Ховати header при скролі вниз, показувати при скролі вгору
        if (scrollTop > lastScrollTop && scrollTop > 200) {
            header.style.transform = 'translateY(-100%)';
        } else {
            header.style.transform = 'translateY(0)';
        }

        lastScrollTop = scrollTop;
    }

    // Додавання CSS для header ефектів
    header.style.transition = 'all 0.3s ease';

    // Throttle для оптимізації
    let ticking = false;
    function requestTick() {
        if (!ticking) {
            requestAnimationFrame(handleHeaderScroll);
            ticking = true;
            setTimeout(() => ticking = false, 16);
        }
    }

    window.addEventListener('scroll', requestTick);
}

/* ===== STAGGERED ANIMATIONS ===== */
function initStaggeredAnimations() {
    if (shouldReduceMotion()) return;

    const staggeredContainers = document.querySelectorAll('.equipment-grid, .about-features__list');

    staggeredContainers.forEach(container => {
        const items = container.children;

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    // Застосувати staggered анімацію до дітей
                    Array.from(items).forEach((item, index) => {
                        setTimeout(() => {
                            item.style.opacity = '1';
                            item.style.transform = 'translateY(0)';
                        }, index * 100);
                    });

                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1
        });

        // Ініціальні стилі для дітей
        Array.from(items).forEach(item => {
            item.style.opacity = '0';
            item.style.transform = 'translateY(30px)';
            item.style.transition = 'all 0.6s ease';
        });

        observer.observe(container);
    });
}

/* ===== LAZY LOADING FOR IMAGES ===== */
function initLazyLoading() {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;

                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.classList.remove('lazy');
                        img.classList.add('lazy-loaded');
                        imageObserver.unobserve(img);
                    }
                }
            });
        });

        const lazyImages = document.querySelectorAll('img[data-src]');
        lazyImages.forEach(img => {
            img.classList.add('lazy');
            imageObserver.observe(img);
        });
    }
}

/* ===== FORM VALIDATION (Enhanced) ===== */
function initFormValidation() {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, textarea, select');

        inputs.forEach(input => {
            // Валідація в реальному часі
            input.addEventListener('blur', function () {
                validateField(this);
            });

            input.addEventListener('input', function () {
                clearFieldError(this);
            });
        });

        // Валідація при сабміті
        form.addEventListener('submit', function (e) {
            let isValid = true;

            inputs.forEach(input => {
                if (!validateField(input)) {
                    isValid = false;
                }
            });

            if (!isValid) {
                e.preventDefault();

                // Показати повідомлення про помилку
                showFormMessage(form, 'Будь ласка, виправте помилки у формі', 'error');

                // Прокрутити до першої помилки
                const firstError = form.querySelector('.field-error');
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
        });
    });
}

function validateField(field) {
    const value = field.value.trim();
    const type = field.type;
    const required = field.hasAttribute('required');

    clearFieldError(field);

    // Перевірка обов'язкових полів
    if (required && !value) {
        showFieldError(field, 'Це поле є обов\'язковим');
        return false;
    }

    // Валідація email
    if (type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            showFieldError(field, 'Введіть коректну email адресу');
            return false;
        }
    }

    // Валідація телефону
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
    field.classList.add('field-error');

    // Створити або оновити повідомлення про помилку
    let errorElement = field.parentNode.querySelector('.error-message');
    if (!errorElement) {
        errorElement = document.createElement('div');
        errorElement.className = 'error-message';
        field.parentNode.appendChild(errorElement);
    }

    errorElement.textContent = message;
    errorElement.style.color = 'var(--promsteel-red-accent)';
    errorElement.style.fontSize = 'var(--text-sm)';
    errorElement.style.marginTop = 'var(--spacing-1)';
}

function clearFieldError(field) {
    field.classList.remove('field-error');

    const errorElement = field.parentNode.querySelector('.error-message');
    if (errorElement) {
        errorElement.remove();
    }
}

function showFormMessage(form, message, type) {
    // Видалити попереднє повідомлення
    const existingMessage = form.querySelector('.form-message');
    if (existingMessage) {
        existingMessage.remove();
    }

    const messageElement = document.createElement('div');
    messageElement.className = `form-message form-message--${type}`;
    messageElement.textContent = message;

    // Стилі повідомлення
    messageElement.style.padding = 'var(--spacing-3) var(--spacing-4)';
    messageElement.style.borderRadius = 'var(--radius-md)';
    messageElement.style.marginBottom = 'var(--spacing-4)';
    messageElement.style.fontWeight = 'var(--font-medium)';

    if (type === 'error') {
        messageElement.style.background = 'rgba(229, 62, 62, 0.1)';
        messageElement.style.color = 'var(--promsteel-red-accent)';
        messageElement.style.border = '1px solid var(--promsteel-red-accent)';
    } else if (type === 'success') {
        messageElement.style.background = 'rgba(52, 168, 83, 0.1)';
        messageElement.style.color = '#34A853';
        messageElement.style.border = '1px solid #34A853';
    }

    form.insertBefore(messageElement, form.firstChild);

    // Автоматично видалити через 5 секунд
    setTimeout(() => {
        if (messageElement.parentNode) {
            messageElement.remove();
        }
    }, 5000);
}

/* ===== UTILITY FUNCTIONS ===== */

// Перевірка настройки користувача щодо зменшення анімацій
function shouldReduceMotion() {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

// Throttle функція для оптимізації подій прокрутки
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
    };
}

// Debounce функція для оптимізації подій зміни розміру
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

/* ===== KEYBOARD NAVIGATION ===== */
document.addEventListener('keydown', function (e) {
    // ESC для закриття мобільного меню
    if (e.key === 'Escape') {
        const nav = document.querySelector('.header__nav');
        const toggle = document.querySelector('.mobile-menu-toggle');

        if (nav && nav.classList.contains('mobile-open')) {
            nav.classList.remove('mobile-open');
            toggle.classList.remove('active');
            document.body.classList.remove('menu-open');
        }
    }
});

/* ===== CONSOLE LOG ===== */
console.log(`
🎨 Promsteel Style Website
🚀 JavaScript успішно завантажено
⚡ Всі анімації та ефекти активні
📱 Адаптивний дизайн готовий
`);

/* ===== ERROR HANDLING ===== */
window.addEventListener('error', function (e) {
    console.error('JavaScript Error:', e.error);
});

window.addEventListener('unhandledrejection', function (e) {
    console.error('Unhandled Promise Rejection:', e.reason);
});