// ASTRIA MODERN SITE INTERACTIONS

document.addEventListener('DOMContentLoaded', () => {
    setupNavigation();
    setupAnimations();
    setupInteractions();
});

// Smooth scrolling
function scrollTo(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}

// Navigation smooth scroll
function setupNavigation() {
    document.querySelectorAll('a[href*="#"]').forEach(link => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');
            if (href.startsWith('#') && href.length > 1) {
                e.preventDefault();
                scrollTo(href.substring(1));
            }
        });
    });
}

// Animations on scroll
function setupAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    document.querySelectorAll('.feature-card, .faq-item, .pricing-card, .funnel-step').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

// Interactions
function setupInteractions() {
    // Checkout
    window.checkout = function(tier) {
        console.log(`Checkout: ${tier}`);
        window.location.href = `/checkout.html?tier=${tier}`;
    };

    // Hover effects
    document.querySelectorAll('.button-primary, .button-outline').forEach(btn => {
        btn.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        btn.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

// Navbar scroll effect
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.08)';
    } else {
        navbar.style.boxShadow = 'none';
    }
});

console.log('✨ Astria modern site loaded');
