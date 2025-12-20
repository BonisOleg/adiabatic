/**
 * Adiabatic Catalog Page JavaScript
 * Accordion functionality for product cards
 */
/* global gtag */

document.addEventListener('DOMContentLoaded', () => {
    // Ініціалізація accordion для кожної картки товару
    const toggleButtons = document.querySelectorAll('.product-toggle');

    toggleButtons.forEach(btn => {
        btn.addEventListener('click', function () {
            const card = this.closest('.product-card');
            const details = card.querySelector('.product-details');
            const icon = this.querySelector('.toggle-icon');

            const isExpanded = details.dataset.expanded === 'true';

            // Опціонально: закрити всі інші картки (коментар знято = акордеон, один відкритий)
            // toggleButtons.forEach(otherBtn => {
            //     if (otherBtn !== this) {
            //         const otherCard = otherBtn.closest('.product-card');
            //         const otherDetails = otherCard.querySelector('.product-details');
            //         const otherIcon = otherBtn.querySelector('.toggle-icon');
            //         
            //         if (otherDetails.dataset.expanded === 'true') {
            //             otherDetails.dataset.expanded = 'false';
            //             otherBtn.setAttribute('aria-expanded', 'false');
            //             if (otherIcon) {
            //                 otherIcon.style.transform = 'rotate(0deg)';
            //             }
            //             otherBtn.innerHTML = 'Детальніше <span class="toggle-icon">▼</span>';
            //         }
            //     }
            // });

            // Toggle поточний стан
            details.dataset.expanded = (!isExpanded).toString();
            this.setAttribute('aria-expanded', (!isExpanded).toString());

            // Animate іконка
            if (icon) {
                icon.style.transform = isExpanded ? 'rotate(0deg)' : 'rotate(180deg)';
            }

            // Змінити текст кнопки
            if (isExpanded) {
                this.innerHTML = 'Детальніше <span class="toggle-icon" style="transform: rotate(0deg);">▼</span>';
            } else {
                this.innerHTML = 'Згорнути <span class="toggle-icon" style="transform: rotate(180deg);">▲</span>';

                // Плавний скрол до картки
                setTimeout(() => {
                    card.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }, 100);
            }

            // Analytics tracking
            const productId = this.dataset.productId;
            if (typeof gtag !== 'undefined' && !isExpanded) {
                gtag('event', 'product_expand', {
                    'event_category': 'catalog',
                    'event_label': productId
                });
            }
        });
    });

    // Галерея: клік на зображення = відкрити в новій вкладці
    const galleryImages = document.querySelectorAll('.gallery-image');

    galleryImages.forEach(img => {
        img.addEventListener('click', function () {
            window.open(this.src, '_blank');

            // Analytics tracking
            if (typeof gtag !== 'undefined') {
                gtag('event', 'gallery_image_click', {
                    'event_category': 'catalog',
                    'event_label': this.alt
                });
            }
        });

        // Додати cursor pointer
        img.style.cursor = 'pointer';
        img.setAttribute('title', 'Клікніть для перегляду у повному розмірі');
    });

    // Головне фото: клік = відкрити в новій вкладці
    const mainImages = document.querySelectorAll('.product-main-image');

    mainImages.forEach(img => {
        img.addEventListener('click', function () {
            window.open(this.src, '_blank');
        });

        img.style.cursor = 'pointer';
        img.setAttribute('title', 'Клікніть для перегляду у повному розмірі');
    });

    // Якщо є якір (#product-slug) в URL, автоматично відкрити цю картку
    const hash = window.location.hash;
    if (hash) {
        const targetCard = document.querySelector(hash);
        if (targetCard && targetCard.classList.contains('product-card')) {
            const toggleBtn = targetCard.querySelector('.product-toggle');
            if (toggleBtn) {
                // Прокрутити до картки
                setTimeout(() => {
                    targetCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }, 300);

                // Відкрити accordion після прокрутки
                setTimeout(() => {
                    toggleBtn.click();
                }, 800);
            }
        }
    }

    // Tracking для кнопок CTA
    const ctaButtons = document.querySelectorAll('.product-actions .btn');

    ctaButtons.forEach(btn => {
        btn.addEventListener('click', function () {
            const card = this.closest('.product-card');
            const productTitle = card ? card.querySelector('.card-title').textContent : 'Unknown';

            if (typeof gtag !== 'undefined') {
                gtag('event', 'cta_click', {
                    'event_category': 'catalog',
                    'event_label': productTitle
                });
            }
        });
    });

    console.log('✅ Catalog page initialized');
});



