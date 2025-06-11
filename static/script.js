document.addEventListener("DOMContentLoaded", () => {
    const productItems = document.querySelectorAll(".product-item");
    const popup = document.createElement("div");
    popup.className = "popup-card hidden";
    document.body.appendChild(popup);

    productItems.forEach(item => {
        item.addEventListener("click", () => {
            const name = item.dataset.name;
            const expires = item.dataset.expires;
            const left = item.dataset.daysLeft;
            const qty = item.dataset.quantity;
            const notes = item.dataset.notes;

            popup.innerHTML = `
                <span id="popup-close" onclick="this.parentElement.classList.add('hidden')">&times;</span>
                <strong>${name}</strong><br>
                do ${expires}<br>
                Pozostało: ${left}<br>
                Ilość: ${qty}<br>
                Opis: ${notes || 'brak'}
            `;
            popup.style.top = `${item.getBoundingClientRect().top + window.scrollY}px`;
            popup.style.left = `${item.getBoundingClientRect().right + 15}px`;
            popup.classList.remove("hidden");
        });
    });

    document.addEventListener("click", (e) => {
        if (!popup.contains(e.target) && !e.target.classList.contains("product-item")) {
            popup.classList.add("hidden");
        }
    });
});
