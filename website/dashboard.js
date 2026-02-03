// ASTRIA DASHBOARD INTERACTIVITY

document.addEventListener('DOMContentLoaded', () => {
    setupNavigation();
    setupSettings();
    simulateLiveData();
});

// Navigation between sections
function setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('.section');

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Remove active from all
            navLinks.forEach(l => l.classList.remove('active'));
            sections.forEach(s => s.classList.remove('active'));
            
            // Add active to clicked
            link.classList.add('active');
            
            // Show corresponding section
            const sectionName = link.dataset.section;
            const sectionElement = document.getElementById(`${sectionName}-section`);
            
            if (sectionElement) {
                sectionElement.classList.add('active');
                
                // Update header
                const pageTitle = sectionName.charAt(0).toUpperCase() + sectionName.slice(1);
                document.getElementById('page-title').textContent = pageTitle;
                document.getElementById('page-subtitle').textContent = getSectionSubtitle(sectionName);
            }
        });
    });

    // Set dashboard as default
    document.querySelector('[data-section="dashboard"]').click();
}

function getSectionSubtitle(section) {
    const subtitles = {
        dashboard: "Welcome back. Here's what Astria found for you this week.",
        leads: "All leads scraped and scored by Astria.",
        emails: "Email performance and metrics.",
        appointments: "Your upcoming discovery calls.",
        reports: "Weekly performance reports.",
        settings: "Configure your Astria account."
    };
    return subtitles[section] || "";
}

// Settings form
function setupSettings() {
    const saveBtn = document.querySelector('.settings-form .btn-primary');
    if (saveBtn) {
        saveBtn.addEventListener('click', () => {
            alert('✅ Settings saved!');
        });
    }
}

// Simulate live data updates
function simulateLiveData() {
    // Update sync status every 5 seconds
    setInterval(() => {
        const statuses = ['Syncing...', 'Synced ✓', 'Checking for new leads...'];
        const status = statuses[Math.floor(Math.random() * statuses.length)];
        document.querySelector('.status-text').textContent = status;
    }, 5000);

    // Simulate activity feed updates
    const activities = [
        { icon: '🔍', text: 'Found <strong>12 new leads</strong> in Miami', time: 'Just now' },
        { icon: '✍️', text: '<strong>8 personalized emails</strong> sent', time: '5 min ago' },
        { icon: '💬', text: '<strong>1 interested reply</strong> received', time: '15 min ago' }
    ];
}

// API Integration ready
async function fetchDashboardData(clientId) {
    // This will connect to your backend API
    // For now, it's mock data
    try {
        const response = await fetch(`/api/clients/${clientId}/dashboard`);
        const data = await response.json();
        updateDashboard(data);
    } catch (error) {
        console.log('Using mock data (API not connected yet)');
    }
}

function updateDashboard(data) {
    // Update KPI cards
    document.querySelector('[data-metric="leads"]').textContent = data.leads_scraped;
    document.querySelector('[data-metric="emails"]').textContent = data.emails_sent;
    document.querySelector('[data-metric="replies"]').textContent = data.replies_interested;
    document.querySelector('[data-metric="appointments"]').textContent = data.appointments_booked;
}

// Export function for later backend integration
window.Astria = {
    fetchDashboardData,
    updateDashboard
};

console.log('✨ Dashboard loaded');
