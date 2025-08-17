# Style.md - Детальна дизайн-система Adiabatic

## 🎨 Кольорова палітра

### Основні кольори (фірмові)
```css
:root {
  /* Фірмові кольори */
  --brand-blue: #1B365D;      /* Основний синій (як промисловий стиль promsteel) */
  --brand-blue-light: #2E5984; /* Світліший синій */
  --brand-red: #C4384D;       /* Акцентний червоний */
  --brand-purple: #8B5FBF;    /* Фіолетовий акцент (з референсних зображень) */
  
  /* Нейтральні кольори */
  --white: #FFFFFF;
  --gray-50: #F8F9FA;
  --gray-100: #F1F3F4;
  --gray-200: #E8EAED;
  --gray-300: #DADCE0;
  --gray-400: #BDC1C6;
  --gray-500: #9AA0A6;
  --gray-600: #80868B;
  --gray-700: #5F6368;
  --gray-800: #3C4043;
  --gray-900: #202124;
  --black: #000000;
  
  /* Семантичні кольори */
  --success: #34A853;
  --warning: #FBBC04;
  --error: #EA4335;
  --info: --brand-blue;
}
```

### Градієнти та ефекти
```css
:root {
  /* Фонові градієнти */
  --gradient-hero: linear-gradient(135deg, rgba(27, 54, 93, 0.8) 0%, rgba(139, 95, 191, 0.6) 100%);
  --gradient-overlay: linear-gradient(180deg, rgba(0, 0, 0, 0.7) 0%, rgba(0, 0, 0, 0.3) 100%);
  --gradient-card: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
  
  /* Тіні */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}
```

## 📝 Типографіка

### Шрифтові родини (з аналізу зображень)
```css
:root {
  /* Основний шрифт - геометричний гротеск */
  --font-primary: 'Inter', 'Montserrat', -apple-system, BlinkMacSystemFont, sans-serif;
  
  /* Акцентний шрифт для заголовків */
  --font-heading: 'Inter', 'Montserrat', sans-serif;
  
  /* Моноширинний для коду */
  --font-mono: 'SF Mono', Monaco, 'Cascadia Code', monospace;
}

/* Імпорт шрифтів */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800&display=swap');
```

### Типографічна шкала
```css
:root {
  /* Розміри шрифтів */
  --text-xs: 0.75rem;    /* 12px */
  --text-sm: 0.875rem;   /* 14px */
  --text-base: 1rem;     /* 16px */
  --text-lg: 1.125rem;   /* 18px */
  --text-xl: 1.25rem;    /* 20px */
  --text-2xl: 1.5rem;    /* 24px */
  --text-3xl: 1.875rem;  /* 30px */
  --text-4xl: 2.25rem;   /* 36px */
  --text-5xl: 3rem;      /* 48px */
  --text-6xl: 3.75rem;   /* 60px */
  --text-7xl: 4.5rem;    /* 72px */
  
  /* Висота рядків */
  --leading-tight: 1.25;
  --leading-normal: 1.5;
  --leading-relaxed: 1.75;
  
  /* Вага шрифту */
  --font-light: 300;
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;
  --font-extrabold: 800;
}
```

### Стилі заголовків (з аналізу зображень)
```css
/* H1 - Hero заголовки */
.heading-hero {
  font-family: var(--font-heading);
  font-size: clamp(2.5rem, 5vw, 4.5rem); /* Респонсивний розмір */
  font-weight: var(--font-bold);
  line-height: var(--leading-tight);
  letter-spacing: -0.02em;
  color: var(--white);
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

/* H2 - Секційні заголовки */
.heading-section {
  font-family: var(--font-heading);
  font-size: clamp(2rem, 4vw, 3rem);
  font-weight: var(--font-semibold);
  line-height: var(--leading-tight);
  color: var(--gray-900);
  margin-bottom: 1.5rem;
}

/* H3 - Підзаголовки */
.heading-subsection {
  font-family: var(--font-heading);
  font-size: clamp(1.5rem, 3vw, 2.25rem);
  font-weight: var(--font-medium);
  line-height: var(--leading-normal);
  color: var(--gray-800);
}

/* Body text */
.text-body {
  font-family: var(--font-primary);
  font-size: var(--text-lg);
  font-weight: var(--font-normal);
  line-height: var(--leading-relaxed);
  color: var(--gray-700);
}

/* Lead text - вступний текст */
.text-lead {
  font-family: var(--font-primary);
  font-size: var(--text-xl);
  font-weight: var(--font-normal);
  line-height: var(--leading-relaxed);
  color: var(--gray-600);
}
```

## 📐 Сітка та відступи

### Responsive Grid
```css
:root {
  /* Контейнери */
  --container-xs: 100%;
  --container-sm: 540px;
  --container-md: 720px;
  --container-lg: 960px;
  --container-xl: 1140px;
  --container-2xl: 1320px;
  
  /* Відступи */
  --spacing-0: 0;
  --spacing-1: 0.25rem;  /* 4px */
  --spacing-2: 0.5rem;   /* 8px */
  --spacing-3: 0.75rem;  /* 12px */
  --spacing-4: 1rem;     /* 16px */
  --spacing-5: 1.25rem;  /* 20px */
  --spacing-6: 1.5rem;   /* 24px */
  --spacing-8: 2rem;     /* 32px */
  --spacing-10: 2.5rem;  /* 40px */
  --spacing-12: 3rem;    /* 48px */
  --spacing-16: 4rem;    /* 64px */
  --spacing-20: 5rem;    /* 80px */
  --spacing-24: 6rem;    /* 96px */
  --spacing-32: 8rem;    /* 128px */
}

/* Grid система */
.container {
  width: 100%;
  margin: 0 auto;
  padding: 0 var(--spacing-4);
}

@media (min-width: 576px) { .container { max-width: var(--container-sm); } }
@media (min-width: 768px) { .container { max-width: var(--container-md); } }
@media (min-width: 992px) { .container { max-width: var(--container-lg); } }
@media (min-width: 1200px) { .container { max-width: var(--container-xl); } }
@media (min-width: 1400px) { .container { max-width: var(--container-2xl); } }
```

### Вертикальний ритм (з аналізу зображень)
```css
/* Секції мають великі відступи */
.section {
  padding: var(--spacing-20) 0; /* 80px top/bottom */
}

.section--large {
  padding: var(--spacing-32) 0; /* 128px для головних секцій */
}

.section--small {
  padding: var(--spacing-16) 0; /* 64px для менших секцій */
}

/* Мобільні відступи менші */
@media (max-width: 768px) {
  .section { padding: var(--spacing-16) 0; }
  .section--large { padding: var(--spacing-20) 0; }
  .section--small { padding: var(--spacing-12) 0; }
}
```

## 🔲 Компоненти

### Кнопки (з аналізу зображень)
```css
/* Базові стилі кнопок */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.75rem 2rem;
  font-family: var(--font-primary);
  font-size: var(--text-base);
  font-weight: var(--font-medium);
  line-height: 1;
  text-decoration: none;
  border-radius: 50px; /* Сильно закруглені кути як на зображеннях */
  border: 2px solid transparent;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 160px;
  text-align: center;
}

/* Основна кнопка */
.btn--primary {
  background: var(--brand-blue);
  color: var(--white);
  border-color: var(--brand-blue);
}

.btn--primary:hover {
  background: var(--brand-blue-light);
  border-color: var(--brand-blue-light);
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

/* Вторинна кнопка */
.btn--secondary {
  background: transparent;
  color: var(--brand-blue);
  border-color: var(--brand-blue);
}

.btn--secondary:hover {
  background: var(--brand-blue);
  color: var(--white);
  transform: translateY(-2px);
}

/* Кнопка на темному фоні */
.btn--light {
  background: var(--white);
  color: var(--brand-blue);
  border-color: var(--white);
}

.btn--light:hover {
  background: var(--gray-100);
  transform: translateY(-2px);
  box-shadow: var(--shadow-xl);
}

/* Розміри кнопок */
.btn--large {
  padding: 1rem 2.5rem;
  font-size: var(--text-lg);
  min-width: 200px;
}

.btn--small {
  padding: 0.5rem 1.5rem;
  font-size: var(--text-sm);
  min-width: 120px;
}
```

### Картки продуктів (з аналізу зображень)
```css
.card {
  background: var(--white);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: var(--shadow-md);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
}

.card:hover {
  transform: translateY(-8px);
  box-shadow: var(--shadow-xl);
}

.card__image {
  width: 100%;
  height: 240px;
  object-fit: cover;
  display: block;
}

.card__content {
  padding: var(--spacing-6);
  flex: 1;
  display: flex;
  flex-direction: column;
}

.card__title {
  font-family: var(--font-heading);
  font-size: var(--text-xl);
  font-weight: var(--font-semibold);
  color: var(--gray-900);
  margin-bottom: var(--spacing-3);
  line-height: var(--leading-tight);
}

.card__description {
  font-family: var(--font-primary);
  font-size: var(--text-base);
  color: var(--gray-600);
  line-height: var(--leading-normal);
  margin-bottom: var(--spacing-4);
  flex: 1;
}

.card__meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: auto;
}

/* Стилі для product grid */
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: var(--spacing-8);
  padding: var(--spacing-8) 0;
}

@media (max-width: 768px) {
  .product-grid {
    grid-template-columns: 1fr;
    gap: var(--spacing-6);
  }
}
```

### Hero секції (з аналізу зображень)
```css
.hero {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background: var(--gray-900);
}

.hero__background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: 1;
}

.hero__overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: var(--gradient-overlay);
  z-index: 2;
}

.hero__content {
  position: relative;
  z-index: 3;
  text-align: center;
  color: var(--white);
  max-width: 800px;
  padding: var(--spacing-8);
}

.hero__subtitle {
  font-family: var(--font-primary);
  font-size: var(--text-lg);
  font-weight: var(--font-medium);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--brand-purple);
  margin-bottom: var(--spacing-4);
}

.hero__title {
  font-family: var(--font-heading);
  font-size: clamp(2.5rem, 5vw, 4.5rem);
  font-weight: var(--font-bold);
  line-height: var(--leading-tight);
  margin-bottom: var(--spacing-6);
  letter-spacing: -0.02em;
}

.hero__description {
  font-family: var(--font-primary);
  font-size: var(--text-xl);
  line-height: var(--leading-relaxed);
  margin-bottom: var(--spacing-8);
  opacity: 0.9;
}

.hero__actions {
  display: flex;
  gap: var(--spacing-4);
  justify-content: center;
  flex-wrap: wrap;
}

/* Мобільна адаптація hero */
@media (max-width: 768px) {
  .hero {
    min-height: 70vh;
  }
  
  .hero__content {
    padding: var(--spacing-6);
  }
  
  .hero__actions {
    flex-direction: column;
    align-items: center;
  }
}
```

### Форми заявок
```css
.form {
  background: var(--white);
  padding: var(--spacing-8);
  border-radius: 16px;
  box-shadow: var(--shadow-lg);
  max-width: 500px;
}

.form__group {
  margin-bottom: var(--spacing-6);
}

.form__label {
  display: block;
  font-family: var(--font-primary);
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  color: var(--gray-700);
  margin-bottom: var(--spacing-2);
}

.form__input {
  width: 100%;
  padding: var(--spacing-4);
  font-family: var(--font-primary);
  font-size: var(--text-base);
  border: 2px solid var(--gray-300);
  border-radius: 8px;
  transition: border-color 0.3s ease;
  background: var(--white);
}

.form__input:focus {
  outline: none;
  border-color: var(--brand-blue);
  box-shadow: 0 0 0 3px rgba(27, 54, 93, 0.1);
}

.form__textarea {
  resize: vertical;
  min-height: 120px;
}

.form__checkbox {
  display: flex;
  align-items: flex-start;
  gap: var(--spacing-3);
}

.form__checkbox input[type="checkbox"] {
  margin-top: 0.25rem;
  accent-color: var(--brand-blue);
}
```

## 🖼️ Зображення та медіа

### Стилі зображень (з аналізу)
```css
/* Основні зображення */
.img-responsive {
  max-width: 100%;
  height: auto;
  display: block;
}

.img-cover {
  object-fit: cover;
  object-position: center;
}

.img-contain {
  object-fit: contain;
}

/* Архітектурні зображення як на референсах */
.img-architectural {
  filter: contrast(1.1) saturate(0.9);
  transition: filter 0.3s ease;
}

.img-architectural:hover {
  filter: contrast(1.2) saturate(1.1);
}

/* Галерея зображень */
.gallery {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--spacing-4);
}

.gallery__item {
  border-radius: 8px;
  overflow: hidden;
  box-shadow: var(--shadow-md);
  transition: transform 0.3s ease;
}

.gallery__item:hover {
  transform: scale(1.05);
}
```

## 📱 iOS Safari специфічні стилі

```css
/* iOS Safari фікси */
@supports (-webkit-touch-callout: none) {
  .hero {
    /* Фікс для 100vh на iOS */
    min-height: -webkit-fill-available;
  }
  
  .btn {
    /* Відключення 3D touch ефекту */
    -webkit-touch-callout: none;
    -webkit-user-select: none;
  }
  
  .form__input {
    /* Відключення zoom при focus */
    font-size: 16px;
    -webkit-appearance: none;
    border-radius: 8px;
  }
}

/* Фікс для landscape орієнтації на iPhone */
@media screen and (max-width: 896px) and (orientation: landscape) {
  .hero {
    min-height: 100vh;
    padding: var(--spacing-4) 0;
  }
}

/* Hover стани тільки для desktop */
@media (hover: hover) and (pointer: fine) {
  .card:hover {
    transform: translateY(-8px);
  }
  
  .btn:hover {
    transform: translateY(-2px);
  }
}
```

## 🎭 Анімації та переходи

```css
/* Базові переходи */
:root {
  --transition-fast: 0.15s ease;
  --transition-normal: 0.3s ease;
  --transition-slow: 0.5s ease;
}

/* Анімації появи контенту */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Класи для JavaScript анімацій */
.fade-in-up {
  animation: fadeInUp 0.6s ease forwards;
}

.fade-in {
  animation: fadeIn 0.4s ease forwards;
}

/* Reduced motion preferences */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

## 🌍 Мультимовна типографіка

```css
/* Спеціальні стилі для різних мов */
:lang(uk) {
  /* Українська - стандартні налаштування */
}

:lang(ru) {
  /* Російська - можливо трохи інший line-height */
  line-height: 1.6;
}

:lang(en) {
  /* Англійська - можливо менший letter-spacing */
  letter-spacing: -0.01em;
}

/* RTL підтримка (на майбутнє) */
[dir="rtl"] {
  text-align: right;
}

[dir="rtl"] .btn {
  margin-left: 0;
  margin-right: var(--spacing-4);
}
```

## 🏭 Промислова тематика (як promsteel.in.ua)

### Технічні характеристики
```css
.tech-specs {
  background: var(--white);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: var(--shadow-md);
}

.tech-specs__table {
  width: 100%;
  border-collapse: collapse;
}

.tech-specs__row {
  border-bottom: 1px solid var(--gray-200);
}

.tech-specs__row:last-child {
  border-bottom: none;
}

.tech-specs__label {
  padding: var(--spacing-4);
  font-family: var(--font-primary);
  font-weight: var(--font-medium);
  color: var(--gray-700);
  background: var(--gray-50);
  width: 40%;
}

.tech-specs__value {
  padding: var(--spacing-4);
  font-family: var(--font-primary);
  color: var(--gray-900);
  font-weight: var(--font-normal);
}

.tech-specs__unit {
  color: var(--gray-500);
  font-size: var(--text-sm);
  margin-left: var(--spacing-1);
}
```

### Каталог обладнання стилі  
```css
.equipment-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--spacing-6);
  padding: var(--spacing-8) 0;
}

.equipment-card {
  background: var(--white);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: var(--shadow-md);
  transition: all 0.3s ease;
  border: 1px solid var(--gray-200);
}

.equipment-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
  border-color: var(--brand-blue);
}

.equipment-card__image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  background: var(--gray-100);
}

.equipment-card__content {
  padding: var(--spacing-6);
}

.equipment-card__title {
  font-family: var(--font-heading);
  font-size: var(--text-lg);
  font-weight: var(--font-semibold);
  color: var(--brand-blue);
  margin-bottom: var(--spacing-3);
}

.equipment-card__description {
  font-family: var(--font-primary);
  font-size: var(--text-sm);
  color: var(--gray-600);
  line-height: var(--leading-normal);
  margin-bottom: var(--spacing-4);
}
```

### Галузі застосування
```css
.industries-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-6);
}

.industry-item {
  text-align: center;
  padding: var(--spacing-6);
  background: var(--white);
  border-radius: 12px;
  box-shadow: var(--shadow-sm);
  transition: all 0.3s ease;
}

.industry-item:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.industry-item__icon {
  width: 64px;
  height: 64px;
  margin: 0 auto var(--spacing-4);
  background: var(--brand-blue);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--white);
  font-size: var(--text-2xl);
}

.industry-item__title {
  font-family: var(--font-heading);
  font-size: var(--text-lg);
  font-weight: var(--font-semibold);
  color: var(--gray-900);
  margin-bottom: var(--spacing-2);
}
```

### Breadcrumbs (як на promsteel)
```css
.breadcrumbs {
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
  margin-bottom: var(--spacing-6);
  font-family: var(--font-primary);
  font-size: var(--text-sm);
}

.breadcrumbs__item {
  color: var(--gray-600);
  text-decoration: none;
}

.breadcrumbs__item:hover {
  color: var(--brand-blue);
}

.breadcrumbs__separator {
  color: var(--gray-400);
}

.breadcrumbs__current {
  color: var(--gray-900);
  font-weight: var(--font-medium);
}
```

### Статистика та досягнення
```css
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-6);
  text-align: center;
}

.stat-item__number {
  font-family: var(--font-heading);
  font-size: var(--text-4xl);
  font-weight: var(--font-bold);
  color: var(--brand-blue);
  display: block;
  margin-bottom: var(--spacing-2);
}

.stat-item__label {
  font-family: var(--font-primary);
  font-size: var(--text-base);
  color: var(--gray-600);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
```

## 📋 Відповідність референсам

### ✅ Прикріплені зображення:
- **Hero з архітектурним фото**: `hero__background` + `hero__overlay`
- **Фіолетові акценти**: `--brand-purple` в hero subtitle
- **Закруглені кнопки**: `border-radius: 50px`
- **"Featured Properties" стиль**: `heading-section` клас
- **Картки з тінями**: `card` компонент з hover ефектами

### ✅ Promsteel.in.ua стиль:
- **Промислова синя палітра**: `--brand-blue #1B365D`
- **Технічні таблиці**: `tech-specs` компонент
- **Каталог обладнання**: `equipment-grid` + `equipment-card`
- **Галузі застосування**: `industries-grid`
- **Breadcrumbs навігація**: `breadcrumbs` компонент
- **Корпоративний стиль**: професійні тіні, типографіка, відступи

Ця дизайн-система поєднує сучасний стиль з прикріплених зображень та промислову естетику promsteel.in.ua, створюючи ідеальний баланс для корпоративного сайту Adiabatic з повною адаптивністю та особливою увагою до iOS Safari.
