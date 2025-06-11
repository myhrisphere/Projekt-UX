document.addEventListener("DOMContentLoaded", function () {
    const popup = document.getElementById("product-popup");
    const popupName = document.getElementById("popup-name");
    const popupExpires = document.getElementById("popup-expires");
    const popupDays = document.getElementById("popup-days");
    const popupQuantity = document.getElementById("popup-quantity");
    const popupNotes = document.getElementById("popup-notes");
    const closeBtn = document.getElementById("popup-close");

    document.querySelectorAll(".product-item").forEach(item => {
        item.addEventListener("click", function (e) {
            e.stopPropagation();

            popupName.textContent = item.dataset.name;
            popupExpires.textContent = item.dataset.expires;
            popupDays.textContent = item.dataset.days;
            popupQuantity.textContent = item.dataset.quantity;
            popupNotes.textContent = item.dataset.notes;

            const rect = item.getBoundingClientRect();

            popup.style.top = (rect.top + window.scrollY) + "px";
            popup.style.left = (rect.right + 10 + window.scrollX) + "px";

            popup.classList.remove("hidden");
        });
    });

    closeBtn.addEventListener("click", () => {
        popup.classList.add("hidden");
    });

    document.addEventListener("click", () => {
        popup.classList.add("hidden");
    });
});
