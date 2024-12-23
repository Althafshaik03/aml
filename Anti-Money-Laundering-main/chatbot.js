
const chatbox = document.getElementById('chatbox');

function appendMessage(sender, message) {
    const div = document.createElement('div');
    div.className = 'message ' + sender;
    div.textContent = (sender === 'user' ? 'You: ' : 'Bot: ') + message;
    chatbox.appendChild(div);
    chatbox.scrollTop = chatbox.scrollHeight;
}

function sendMessage() {
    const userInput = document.getElementById('userInput');
    const message = userInput.value.trim();
    if (!message) return;

    appendMessage('user', message);
    userInput.value = '';

    fetch('http://127.0.0.1:5001/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: message })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Network response was not ok.");
        }
        return response.json();
    })
    .then(data => {
        if (data.message) {
            appendMessage('bot', data.message);
        }
        if (data.transactions) {
            data.transactions.forEach(transaction => {
                appendMessage('bot', JSON.stringify(transaction));
            });
        }
    })
    .catch(error => {
        appendMessage('bot', 'Error: ' + error.message);
    });
}
