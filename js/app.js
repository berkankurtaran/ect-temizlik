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

    // 3D Robot Vacuum Animation Injection
    const robotVacuum = document.createElement('div');
    robotVacuum.className = 'robot-vacuum-wrapper';
    robotVacuum.innerHTML = `
        <div class="robot-vacuum-3d">
            <div class="rv-clean-trail">
                <span class="rv-sparkle s1">✦</span>
                <span class="rv-sparkle s2">✧</span>
                <span class="rv-sparkle s3">✦</span>
            </div>
            <div class="rv-floor-shadow"></div>
            <div class="rv-side-brush left"></div>
            <div class="rv-side-brush right"></div>
            <div class="rv-chassis">
                <div class="rv-bumper"></div>
                <div class="rv-top-deck">
                    <div class="rv-led-ring"></div>
                    <div class="rv-lidar">
                        <div class="rv-lidar-cap"></div>
                    </div>
                </div>
            </div>
        </div>
    `;
    document.body.appendChild(robotVacuum);
});
