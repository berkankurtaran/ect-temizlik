document.addEventListener('DOMContentLoaded', () => {
    // Welcome Splash Screen
    const splashScreen = document.getElementById('splash-screen');
    if (splashScreen) {
        setTimeout(() => {
            splashScreen.classList.add('hidden');
            setTimeout(() => {
                splashScreen.remove();
            }, 800);
        }, 1500);
    }

    // Navbar scroll effect — passive listener for iOS performance
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }, { passive: true });

    // Mobile Menu Toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');

    if (mobileMenuBtn && navLinks) {
        // Menü aç/kapat
        mobileMenuBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            const isOpen = navLinks.classList.toggle('active');
            // Menü açıkken sayfanın kaymasını engelle
            document.body.classList.toggle('menu-open', isOpen);
            mobileMenuBtn.textContent = isOpen ? '✕' : '☰';
        });

        // Nav linklerine tıklayınca menüyü kapat
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
                document.body.classList.remove('menu-open');
                mobileMenuBtn.textContent = '☰';
            });
        });

        // Menü dışına tıklayınca kapat
        document.addEventListener('click', (e) => {
            if (!navbar.contains(e.target) && navLinks.classList.contains('active')) {
                navLinks.classList.remove('active');
                document.body.classList.remove('menu-open');
                mobileMenuBtn.textContent = '☰';
            }
        });
    }

    // Robot Vacuum Animation Injection
    const robotVacuum = document.createElement('div');
    robotVacuum.className = 'robot-vacuum-wrapper';
    robotVacuum.innerHTML = '<div class="robot-vacuum"></div>';
    document.body.appendChild(robotVacuum);
});
