/* ===== DESKTOP ANIMATED MENU ===== */

class AnimatedDesktopMenu {
    constructor() {
        this.isMenuOpen = false;
        this.isAnimating = false;
        this.isMobile = window.innerWidth < 768;

        this.burger = document.querySelector('.desktop-burger-btn');
        this.logo = document.querySelector('.logo');
        this.menu = document.querySelector('.animated-desktop-menu');

        this.init();
    }

    init() {
        console.log('🔧 AnimatedDesktopMenu.init() called');
        console.log('Elements found:', {
            burger: !!this.burger,
            logo: !!this.logo,
            menu: !!this.menu
        });
        console.log('Is mobile?', this.isMobile);

        if (!this.burger || !this.logo || !this.menu) {
            console.error('❌ Missing required elements for desktop menu');
            return;
        }

        // Only initialize on desktop
        if (this.isMobile) {
            console.log('📱 Mobile detected, not initializing desktop menu');
            return;
        }

        this.setupEventListeners();
        this.setupResponsive();
        console.log('✅ Desktop Animated Menu initialized successfully');
    }

    setupEventListeners() {
        // Burger button click
        this.burger.addEventListener('click', (e) => {
            e.preventDefault();
            this.handleBurgerClick();
        });

        // Close menu when clicking menu links
        const menuLinks = this.menu.querySelectorAll('.animated-nav-link');
        menuLinks.forEach(link => {
            link.addEventListener('click', () => {
                this.closeMenu();
            });
        });

        // Close menu on Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isMenuOpen) {
                this.closeMenu();
            }
        });
    }

    setupResponsive() {
        // Handle window resize
        window.addEventListener('resize', debounce(() => {
            const newIsMobile = window.innerWidth < 768;

            if (newIsMobile !== this.isMobile) {
                this.isMobile = newIsMobile;

                // Close menu if switching to mobile
                if (this.isMobile && this.isMenuOpen) {
                    this.closeMenu(true); // Force close without animation
                }
            }
        }, 250));
    }

    handleBurgerClick() {
        if (this.isAnimating) return;

        if (this.isMenuOpen) {
            this.closeMenu();
        } else {
            this.openMenu();
        }
    }

    openMenu() {
        if (this.isAnimating || this.isMenuOpen || this.isMobile) return;

        this.isAnimating = true;
        this.isMenuOpen = true;

        // Update burger button
        this.burger.classList.add('active');
        this.burger.setAttribute('aria-expanded', 'true');

        // Start logo animation (moving LEFT from right position)
        this.logo.classList.add('moving-left');

        // Show menu after logo starts moving
        setTimeout(() => {
            this.menu.classList.add('active');
        }, 200);

        // Animation complete
        setTimeout(() => {
            this.isAnimating = false;
        }, 1000);

        console.log('📤 Desktop menu opened');
    }

    closeMenu(force = false) {
        if (!force && (this.isAnimating || !this.isMenuOpen)) return;

        this.isAnimating = true;
        this.isMenuOpen = false;

        // Hide menu first
        this.menu.classList.remove('active');

        // Start logo return animation (moving RIGHT back to original position)
        setTimeout(() => {
            this.logo.classList.remove('moving-left');
            this.logo.classList.add('moving-right');
        }, 100);

        // Reset burger button
        setTimeout(() => {
            this.burger.classList.remove('active');
            this.burger.setAttribute('aria-expanded', 'false');
        }, 300);

        // Clean up logo classes
        setTimeout(() => {
            this.logo.classList.remove('moving-right');
            this.isAnimating = false;
        }, 700);

        console.log('📥 Desktop menu closed');
    }

    // Public methods for external access
    isOpen() {
        return this.isMenuOpen;
    }

    toggle() {
        this.handleBurgerClick();
    }
}

/* ===== INIT DESKTOP ANIMATED MENU ===== */
function initDesktopAnimatedMenu() {
    console.log('🔍 Checking desktop menu initialization...');
    console.log('Window width:', window.innerWidth);
    console.log('Is desktop?', window.innerWidth >= 768);

    // Only initialize on desktop
    if (window.innerWidth >= 768) {
        console.log('🎯 Initializing desktop animated menu...');
        window.animatedDesktopMenu = new AnimatedDesktopMenu();
    } else {
        console.log('📱 Mobile detected, skipping desktop menu');
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', initDesktopAnimatedMenu);
