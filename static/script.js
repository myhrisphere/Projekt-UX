document.addEventListener('DOMContentLoaded', function () {
    const productItems = document.querySelectorAll('.product-item');

    productItems.forEach(item => {
        const popup = item.querySelector('.popup-card');
        const closeBtn = popup.querySelector('#popup-close');

        item.addEventListener('click', function (e) {
            if (e.target.closest('.delete-btn')) return;

            // Hide all other popups
            document.querySelectorAll('.popup-card').forEach(p => p.classList.add('hidden'));

            // Get position relative to the viewport
            const rect = item.getBoundingClientRect();

            // Position the popup beside the product box
            popup.style.position = 'fixed';
            popup.style.top = `${rect.top}px`;
            popup.style.left = `${rect.right + 10}px`;
            popup.classList.remove('hidden');
        });

        if (closeBtn) {
            closeBtn.addEventListener('click', function (e) {
                e.stopPropagation();
                popup.classList.add('hidden');
            });
        }
    });

    document.addEventListener('click', function (e) {
        if (!e.target.closest('.product-item') && !e.target.closest('.popup-card')) {
            document.querySelectorAll('.popup-card').forEach(p => p.classList.add('hidden'));
        }
    });
});
