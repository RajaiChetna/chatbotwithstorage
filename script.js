async function sendMessage() {
    const userInput = document.getElementById("user-input").value;
    if (!userInput) return;

    displayMessage(userInput, "user");
    document.getElementById("user-input").value = '';

    const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userInput })
    });

    const data = await response.json();
    displayMessage(data.reply, "bot");
}

function displayMessage(message, sender) {
    const chatBox = document.getElementById("chat-box");
    const div = document.createElement("div");
    div.className = sender;
    div.textContent = message;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}