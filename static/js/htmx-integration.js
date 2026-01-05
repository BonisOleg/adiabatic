'use strict';

/**
 * HTMX Integration для Adiabatic
 * CSRF token та error handling
 */

// CSRF token для всіх HTMX запитів
document.body.addEventListener('htmx:configRequest', (event) => {
  const csrfToken = document.querySelector('meta[name="csrf-token"]');
  if (csrfToken) {
    event.detail.headers['X-CSRFToken'] = csrfToken.getAttribute('content');
  }
});

// Обробка помилок мережі
document.body.addEventListener('htmx:sendError', (event) => {
  console.error('HTMX Send Error:', event.detail);
  showNotification('Помилка відправки запиту. Перевірте з\'єднання.', 'error');
});

// Обробка помилок відповіді сервера
document.body.addEventListener('htmx:responseError', (event) => {
  console.error('HTMX Response Error:', event.detail);
  const status = event.detail.xhr.status;
  
  let message = 'Помилка завантаження даних.';
  if (status === 404) message = 'Сторінка не знайдена.';
  else if (status === 500) message = 'Помилка сервера. Спробуйте пізніше.';
  else if (status === 403) message = 'Доступ заборонено.';
  
  showNotification(message, 'error');
});

// Після успішної заміни контенту
document.body.addEventListener('htmx:afterSwap', (event) => {
  console.log('HTMX content swapped:', event.detail.target);
  
  // Ре-ініціалізація компонентів якщо потрібно
  if (event.detail.target.querySelector('form')) {
    // Можна додати ре-ініціалізацію валідації форм
  }
});

// Utility: показати notification
function showNotification(message, type) {
  const notification = document.createElement('div');
  notification.className = `notification notification--${type}`;
  notification.textContent = message;
  notification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 1rem 1.5rem;
    background: ${type === 'error' ? 'var(--secondary)' : 'var(--primary)'};
    color: var(--white);
    border-radius: var(--radius);
    box-shadow: var(--shadow-lg);
    z-index: 9999;
    animation: slideIn 0.3s ease;
  `;
  
  document.body.appendChild(notification);
  
  setTimeout(() => {
    notification.style.animation = 'slideOut 0.3s ease';
    setTimeout(() => notification.remove(), 300);
  }, 5000);
}

console.log('✅ HTMX integration loaded');






