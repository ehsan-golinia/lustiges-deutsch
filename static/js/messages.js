document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.auto-close');

    alerts.forEach(alert => {
        // Wait 2 seconds before starting to remove
        setTimeout(() => {
            // Add removing class for slide out animation
            alert.classList.add('removing');

            // Remove the element after animation completes
            setTimeout(() => {
                alert.remove();
            }, 500); // 500ms matches the slideOut animation duration
        }, 4000); // 2000ms = 2 seconds display time
    });
});
