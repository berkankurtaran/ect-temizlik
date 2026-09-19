document.addEventListener('DOMContentLoaded', () => {
    // Welcome Splash Screen
    const splashScreen = document.getElementById('splash-screen');
    if (splashScreen) {
        // Hide splash screen after a short delay (1.5s) to allow animation to play
        setTimeout(() => {
            splashScreen.classList.add('hidden');
            // Remove from DOM after transition (0.8s)
            setTimeout(() => {
                splashScreen.remove();
            }, 800);
        }, 1500);
    }

    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.add('scrolled'); // keep it or adjust padding
            if (window.scrollY === 0) {
                navbar.classList.remove('scrolled');
            }
        }
    });

    // Mobile Menu Toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');

    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });
    }

    // Cleaning Man Animation Injection
    const cleaningMan = document.createElement('div');
    cleaningMan.className = 'cleaning-man';
    cleaningMan.innerHTML = '<span class="man-emoji">🚶‍♂️</span><span class="mop-emoji">🧹</span>';
    document.body.appendChild(cleaningMan);
});
