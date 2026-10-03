// landing.js — "See how it works" video modal

(function () {
    const openBtn = document.getElementById("how-it-works-btn");
    const modal = document.getElementById("how-it-works-modal");
    if (!openBtn || !modal) return;

    const closeBtn = modal.querySelector(".video-modal-close");
    const iframe = modal.querySelector("iframe");

    openBtn.addEventListener("click", function (event) {
        event.preventDefault();
        // Load the video only when the modal opens
        iframe.src = iframe.dataset.src;
        modal.showModal();
    });

    closeBtn.addEventListener("click", function () {
        modal.close();
    });

    // Clicks on the backdrop land on the <dialog> itself, not its content
    modal.addEventListener("click", function (event) {
        if (event.target === modal) modal.close();
    });

    // Fires for every way of closing (button, backdrop, Esc).
    // Clearing the src unloads the player so the video stops.
    modal.addEventListener("close", function () {
        iframe.src = "";
    });
})();
