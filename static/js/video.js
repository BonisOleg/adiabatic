/* ===== VIDEO FUNCTIONALITY ===== */

document.addEventListener('DOMContentLoaded', function () {
    initVideoRotation();
    initFixedVideoBackground();
});

/* ===== VIDEO ROTATION FOR HOME PAGE ===== */
function initVideoRotation() {
    const videoElements = document.querySelectorAll('.hero-video--rotating');

    if (videoElements.length < 2) {
        console.log('🎬 Video rotation not initialized - need 2 videos');
        return;
    }

    console.log('🎬 Initializing video rotation with', videoElements.length, 'videos');

    let currentIndex = 0;
    let transitionTimeout = null;

    // Встановлюємо початковий стан
    videoElements.forEach((video, index) => {
        if (index === 0) {
            video.classList.remove('hero-video--hidden');
            video.play();
            setupVideoEndTransition(video, index);
        } else {
            video.classList.add('hero-video--hidden');
            video.pause();
        }
    });

    function setupVideoEndTransition(video, videoIndex) {
        // Очищуємо попередній таймер
        if (transitionTimeout) {
            clearTimeout(transitionTimeout);
        }

        // Функція для відстеження часу відео
        function checkVideoTime() {
            const currentTime = video.currentTime;
            const duration = video.duration;

            // Якщо до кінця відео залишилася 1 секунда
            if (duration && currentTime >= duration - 1) {
                console.log(`🎬 Video ${videoIndex + 1} ending in 1 second, starting transition...`);
                startTransition(videoIndex);
                return;
            }

            // Перевіряємо кожні 100мс
            if (!video.paused) {
                setTimeout(checkVideoTime, 100);
            }
        }

        // Запускаємо відстеження часу
        checkVideoTime();

        // Додатковий обробник на випадок завершення відео
        video.addEventListener('ended', () => {
            console.log(`🎬 Video ${videoIndex + 1} ended naturally`);
            startTransition(videoIndex);
        });
    }

    function startTransition(fromIndex) {
        const currentVideo = videoElements[fromIndex];
        const nextIndex = (fromIndex + 1) % videoElements.length;
        const nextVideo = videoElements[nextIndex];

        console.log(`🎬 Starting transition from video ${fromIndex + 1} to video ${nextIndex + 1}`);

        // Підготовуємо наступне відео
        nextVideo.currentTime = 0;
        nextVideo.classList.remove('hero-video--hidden');
        nextVideo.play();

        // Починаємо плавний перехід (1 секунда)
        setTimeout(() => {
            currentVideo.classList.add('hero-video--hidden');

            // Паузимо попереднє відео після переходу
            setTimeout(() => {
                currentVideo.pause();
                currentVideo.currentTime = 0; // Скидаємо на початок
            }, 1000); // Через 1 секунду після початку fade-out

            currentIndex = nextIndex;

            // Налаштовуємо відстеження для нового активного відео
            setupVideoEndTransition(nextVideo, nextIndex);

            console.log(`✅ Transitioned to video ${nextIndex + 1}`);
        }, 100);
    }

    // Додаємо обробку помилок для відео
    videoElements.forEach((video, index) => {
        video.addEventListener('error', function (e) {
            console.error(`❌ Video ${index + 1} error:`, e);

            // При помилці переключаємося на наступне відео
            if (index === currentIndex) {
                setTimeout(() => startTransition(index), 1000);
            }
        });

        video.addEventListener('loadstart', function () {
            console.log(`📁 Video ${index + 1} loading started`);
        });

        video.addEventListener('canplay', function () {
            console.log(`✅ Video ${index + 1} ready to play`);
        });

        // Важливо для безперервного відтворення
        video.addEventListener('loadedmetadata', function () {
            console.log(`📊 Video ${index + 1} metadata loaded, duration: ${video.duration}s`);
        });
    });

    // Мобільна оптимізація
    const isMobile = window.innerWidth <= 768 || 'ontouchstart' in window;
    if (isMobile) {
        // На мобільних пристроях паузимо відео для економії батареї
        videoElements.forEach(video => {
            video.muted = true;
            video.pause();
            video.style.opacity = '0.7';
        });

        // Показуємо лише перше відео як статичне зображення
        videoElements[0].classList.remove('hero-video--hidden');
        console.log('📱 Mobile detected - video rotation disabled for battery optimization');
    }

    // iOS Safari оптимізації
    const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent);
    if (isIOS) {
        videoElements.forEach(video => {
            video.playsInline = true;
            video.muted = true;
            video.setAttribute('webkit-playsinline', 'true');
        });
        console.log('🍎 iOS Safari optimizations applied');
    }

    console.log('🎬 Video rotation initialized successfully');
}

/* ===== FIXED VIDEO BACKGROUND EFFECT ===== */
function initFixedVideoBackground() {
    console.log('🎯 Initializing fixed video background...');

    // Ensure sections stack properly over video
    const sections = document.querySelectorAll('.section:not(.hero)');
    sections.forEach((section, index) => {
        section.style.position = 'relative';
        section.style.zIndex = 10 + index;
        section.style.background = section.style.background || 'var(--white)';
    });

    // Header transparency effect on scroll
    const header = document.querySelector('.header');
    if (header) {
        window.addEventListener('scroll', function () {
            const scrolled = window.pageYOffset;
            if (scrolled > 100) {
                header.style.background = 'rgba(49, 60, 72, 0.95)';
                header.style.backdropFilter = 'blur(10px)';
            } else {
                header.style.background = 'var(--primary)';
                header.style.backdropFilter = 'none';
            }
        }, { passive: true });
    }

    // Video optimization for mobile
    const heroVideo = document.querySelector('.hero-video');
    const isTouch = 'ontouchstart' in window;
    const isMobile = window.innerWidth <= 768;

    if (heroVideo) {
        if (isTouch || isMobile) {
            // Pause video on mobile to save battery
            heroVideo.pause();
            heroVideo.style.opacity = '0.8';
            console.log('📱 Video paused on mobile device');
        } else {
            console.log('🎬 Video playing on desktop');
        }
    }

    console.log('✅ Fixed video background initialized');
}
