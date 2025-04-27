async function sendMessage() {
  const userInput = document.getElementById("user-input").value;
  if (!userInput) return;

  const chatWindow = document.getElementById("chat-window");
  const userMessage = document.createElement("div");
  userMessage.className = "message user-message";
  userMessage.textContent = userInput;
  chatWindow.appendChild(userMessage);

  document.getElementById("user-input").value = "";

  try {
    const response = await fetch("http://localhost:3000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userInput }),
    });
    const data = await response.json();

    const botMessage = document.createElement("div");
    botMessage.className = "message bot-message";
    botMessage.textContent = data.reply;
    chatWindow.appendChild(botMessage);

    chatWindow.scrollTop = chatWindow.scrollHeight;
  } catch (error) {
    console.error("Error:", error);
  }
}

// Add Enter key support
document
  .getElementById("user-input")
  .addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      sendMessage();
    }
  });
