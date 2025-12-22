# Скрипти автоматичного контролю якості коду

Ця директорія містить bash-скрипти для автоматичної перевірки та виправлення порушень правил кросплатформенної веб-розробки.

## Структура скриптів

### Перевірки

#### `check-all-rules.sh`
Запускає всі перевірки проекту:
- Django template tags
- HTML custom rules
- CSS custom rules
- JavaScript custom rules
- Stylelint
- ESLint
- HTMLHint

**Використання:**
```bash
bash scripts/check-all-rules.sh
# або
npm run check:rules
```

#### `check-html-rules.sh`
Перевіряє HTML правила:
- viewport meta атрибути (viewport-fit=cover, interactive-widget=resizes-content)
- Відсутність inline styles
- Відсутність inline event handlers
- inputmode для tel/number inputs
- video теги (poster, playsinline, muted)
- script теги (defer/async)
- CSRF meta tag

**Використання:**
```bash
bash scripts/check-html-rules.sh
```

#### `check-css-rules.sh`
Перевіряє CSS правила:
- 100vh має fallback 100dvh
- safe-area-inset використання
- font-size в rem (warning)
- flex shorthand (flex: 1 0 0)
- :hover в @media (hover: hover)
- overscroll-behavior на body
- touch-action: manipulation
- backdrop-filter з -webkit- prefix
- Відсутність !important

**Використання:**
```bash
bash scripts/check-css-rules.sh
```

#### `check-js-rules.sh`
Перевіряє JavaScript правила:
- Відсутність var
- pageshow event listener
- Відсутність eval()
- HTMX integration

**Використання:**
```bash
bash scripts/check-js-rules.sh
```

#### `check_template_tags.sh`
Перевіряє Django template tags на розривання:
- {{ }} теги мають бути на одному рядку
- {% %} теги мають бути на одному рядку

**Використання:**
```bash
bash scripts/check_template_tags.sh
```

### Автоматичні виправлення

#### `fix-rules.sh`
Автоматично виправляє деякі порушення:
- Видаляє inline `style=""` атрибути
- Додає `inputmode="tel"` до tel inputs
- Виправляє `flex: 1;` → `flex: 1 0 0;`

**Використання:**
```bash
bash scripts/fix-rules.sh
# або
npm run fix:rules
```

**Увага:** Скрипт створює backup файли (.bak), які автоматично видаляються після виконання.

### Git Hooks

#### `pre-commit-hook.sh`
Git pre-commit hook, що запускається автоматично перед commit:
- Перевіряє тільки staged files
- Блокує commit при будь-яких помилках
- Показує рекомендації для виправлення

**Налаштування:**
```bash
# Hook вже налаштований через Husky
# Файл: .husky/pre-commit
```

## npm scripts

У `package.json` доступні наступні команди:

```bash
# Запуск всіх перевірок
npm run check:rules

# Автоматичне виправлення
npm run fix:rules

# Окремі лінтери
npm run lint:css
npm run lint:js
npm run lint:html

# Автоматичне виправлення лінтерів
npm run lint:fix
```

## Приклади використання

### Перевірка перед commit
```bash
npm run check:rules
```

### Виправлення простих помилок
```bash
npm run fix:rules
```

### Перевірка конкретного файлу
```bash
npx stylelint static/css/components.css
npx eslint static/js/base.js
npx htmlhint templates/base.html
```

## Troubleshooting

### Скрипт не виконується
```bash
chmod +x scripts/*.sh
```

### Git hook не спрацьовує
```bash
# Перевірте чи існує .husky/pre-commit
ls -la .husky/pre-commit

# Перевірте права доступу
chmod +x .husky/pre-commit
```

### Лінтери не знаходять файли
Переконайтесь що ви знаходитесь в корені проекту:
```bash
cd /path/to/adiabatic
npm run check:rules
```

## Додаткова інформація

Всі правила базуються на інструкції "Повна інструкція налаштування системи автоматичного контролю якості коду" та охоплюють 110+ правил для кросплатформенної веб-розробки.





