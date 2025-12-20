/* ===== ADIABATIC LEAD FORM JAVASCRIPT ===== */
/* global validateForm, gtag */

document.addEventListener('DOMContentLoaded', () => {
    initLeadForm();
    console.log('📝 Lead form JavaScript loaded');
});

function initLeadForm() {
    const leadForm = document.getElementById('leadForm');
    if (!leadForm) return;

    // Form validation is handled by form-validation.js

    // Handle form submission
    leadForm.addEventListener('submit', function (e) {
        e.preventDefault();

        if (validateForm(this)) {
            submitLeadForm(this);
        }
    });
}

function submitLeadForm(form) {
    const formData = new FormData(form);
    const submitButton = form.querySelector('button[type="submit"]');

    // Show loading state
    setLoadingState(submitButton, true);
    hideMessages();

    // Submit via AJAX
    fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        }
    })
        .then(response => response.json())
        .then(data => {
            setLoadingState(submitButton, false);

            if (data.success) {
                showSuccessMessage('Дякуємо! Ваша заявка успішно відправлена. Ми зв\'яжемося з вами найближчим часом.');
                form.reset();

                // Track successful form submission
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'form_submit_success', {
                        event_category: 'engagement',
                        event_label: 'lead_form'
                    });
                }
            } else {
                showErrorMessage(data.message || 'Помилка відправки форми. Спробуйте ще раз.');
            }
        })
        .catch(error => {
            console.error('Form submission error:', error);
            setLoadingState(submitButton, false);
            showErrorMessage('Помилка відправки форми. Перевірте підключення до інтернету.');
        });
}

function setLoadingState(button, isLoading) {
    if (!button) return;

    if (isLoading) {
        button.disabled = true;
        button.classList.add('loading');
        button.dataset.originalText = button.textContent;
        button.textContent = 'Відправляємо...';
    } else {
        button.disabled = false;
        button.classList.remove('loading');
        button.textContent = button.dataset.originalText || 'Відправити заявку';
    }
}

function showSuccessMessage(message) {
    const container = getOrCreateMessageContainer();
    container.innerHTML = `
        <div class="form-success show">
            <strong>Успіх!</strong> ${message}
        </div>
    `;
    container.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

function showErrorMessage(message) {
    const container = getOrCreateMessageContainer();
    container.innerHTML = `
        <div class="form-error show">
            <strong>Помилка!</strong> ${message}
        </div>
    `;
    container.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

function hideMessages() {
    const container = document.getElementById('form-messages');
    if (container) {
        container.innerHTML = '';
    }
}

function getOrCreateMessageContainer() {
    let container = document.getElementById('form-messages');
    if (!container) {
        container = document.createElement('div');
        container.id = 'form-messages';

        const form = document.getElementById('leadForm');
        if (form) {
            form.parentNode.insertBefore(container, form);
        }
    }
    return container;
}

// Download tracking functionality is handled by base.js
