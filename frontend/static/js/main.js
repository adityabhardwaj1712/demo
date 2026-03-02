const protocol = window.location.protocol === "https:" ? "wss://" : "ws://";

try {
    const socket = new WebSocket(
        protocol + window.location.host + "/ws/notifications/"
    );

    socket.onmessage = function(e) {
        const data = JSON.parse(e.data);

        const toastEl = document.getElementById('liveToast');
        const toastBody = document.getElementById('toast-body');

        toastBody.innerText = data.message;
        const toast = new bootstrap.Toast(toastEl);
        toast.show();

        const countEl = document.getElementById("notification-count");
        let current = parseInt(countEl.innerText) || 0;
        countEl.innerText = current + 1;
    };

} catch (err) {
    console.log("WebSocket not connected.");
}