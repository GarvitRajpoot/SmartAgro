document.addEventListener("DOMContentLoaded", () => {

  const BACKEND = "http://127.0.0.1:8000";

  const chatbox = document.getElementById("chatbox");
  const chatForm = document.getElementById("chat-form");
  const messageInput = document.getElementById("message-input");
  const suggestionChipsContainer = document.getElementById("suggestion-chips");

  let chatHistory = [];

  function formatResponse(text) {
    return text
      .replace(/\*\*(.*?)\*\*/g, "<b>$1</b>")
      .replace(/\* /g, "• ")
      .replace(/\n/g, "<br>");
  }

  function addMessage(text, sender) {
    const msg = document.createElement("div");
    msg.className = `chat ${sender}`;
    msg.innerHTML = formatResponse(text);
    chatbox.appendChild(msg);
    chatbox.scrollTop = chatbox.scrollHeight;
  }

  function showLoading() {
    const loader = document.createElement("div");
    loader.className = "chat bot loading-indicator";
    loader.id = "loading";
    loader.innerHTML = `<span></span><span></span><span></span>`;
    chatbox.appendChild(loader);
    chatbox.scrollTop = chatbox.scrollHeight;
  }

  function removeLoading() {
    const loader = document.getElementById("loading");
    if (loader) loader.remove();
  }

  async function getAIResponse(message) {
  try {
    chatHistory.push({ role: "user", text: message });

    const response = await fetch("http://127.0.0.1:8000/api/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        message: message,
        history: chatHistory   
      })
    });

    const data = await response.json();

    chatHistory.push({ role: "assistant", text: data.reply });

    return data.reply || "No response";

  } catch (error) {
    console.error(error);
    return "⚠️ Error connecting to server";
  }
}

  async function sendMessage(message) {
    if (!message.trim()) return;

    addMessage(message, "user");
    messageInput.value = "";
    suggestionChipsContainer.style.display = "none";

    showLoading();

    const reply = await getAIResponse(message);

    removeLoading();
    addMessage(reply, "bot");
  }

  chatForm.addEventListener("submit", (e) => {
    e.preventDefault();
    sendMessage(messageInput.value);
  });

  suggestionChipsContainer.addEventListener("click", (e) => {
    if (e.target.classList.contains("chip")) {
      sendMessage(e.target.textContent);
    }
  });

  setTimeout(() => {
    addMessage("Hello! I'm the SmartAgro Assistant 🌱. How can I help you today?", "bot");
  }, 500);

});