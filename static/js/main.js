/**
 * LendIt P2P Marketplace — Main JavaScript
 * Handles: alert auto-hide, mobile nav toggle.
 */

document.addEventListener('DOMContentLoaded', () => {
    // -----------------------------------------------------------------------
    // Auto-hide alert messages after 5 seconds
    // -----------------------------------------------------------------------
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach((alert) => {
        setTimeout(() => {
            alert.classList.add('fade-out');
            setTimeout(() => alert.remove(), 400);
        }, 5000);
    });

    // -----------------------------------------------------------------------
    // Mobile navigation toggle
    // -----------------------------------------------------------------------
    const navToggle = document.getElementById('navToggle');
    const navLinks = document.getElementById('navLinks');

    if (navToggle && navLinks) {
        navToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });

        // Close nav when clicking a link (mobile)
        navLinks.querySelectorAll('.nav-link').forEach((link) => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
            });
        });
    }
});
