// Используем глобальную переменную sessionId
const url = `ws://${window.location.host}/ws/${sessionId}`;
const ws = new WebSocket(url);

ws.onmessage = function(event) {
    const messages = document.getElementById('messages');
    const message = document.createElement('div');
    message.textContent = event.data;
    messages.appendChild(message);
};

function sendMessage() {
    const input = document.getElementById("messageInput");
    ws.send(input.value);
    input.value = '';
}
