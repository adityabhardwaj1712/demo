const protocol = window.location.protocol === "https:" ? "wss://" : "ws://";

try {
    const socket = new WebSocket(
        protocol + window.location.host + "/ws/notifications/"
    );

    socket.onmessage = function(e) {
        const data = JSON.parse(e.data);

        document.getElementById("toast-body").innerText = data.message;
        const toast = new bootstrap.Toast(document.getElementById('liveToast'));
        toast.show();

        let countElement = document.getElementById("notification-count");
        let currentCount = parseInt(countElement.innerText) || 0;
        countElement.innerText = currentCount + 1;
    };
} catch (err) {}

function showLoader() {
    document.getElementById("loader").style.display = "flex";
}

function hideLoader() {
    document.getElementById("loader").style.display = "none";
}