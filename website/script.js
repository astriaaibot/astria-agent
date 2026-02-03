// ASTRIA WEBSITE SCRIPT

// Smooth scroll to section
function scrollToContact() {
    const contactSection = document.getElementById('contact');
    contactSection.scrollIntoView({ behavior: 'smooth' });
}

// Checkout function (Stripe integration)
function checkout(tier) {
    console.log(`Checkout: ${tier}`);
    window.location.href = `/checkout.html?tier=${tier}`;
}

// Navbar scroll effect
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.1)';
    } else {
        navbar.style.boxShadow = 'none';
    }
});

// Animate elements on scroll
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

// Observe all feature cards
document.querySelectorAll('.feature-card, .step, .faq-item, .pricing-card').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});

// Add CTA tracking (optional)
document.querySelectorAll('a[href*="cal.com"]').forEach(link => {
    link.addEventListener('click', () => {
        console.log('CTA clicked: Demo booking');
        // Track event here if using analytics
    });
});

console.log('✨ Astria website loaded');
