const chatMessages = document.getElementById("chatMessages");
const userInput = document.getElementById("userInput");
const sendButton = document.getElementById("sendButton");
function addMessage(text, type) {
  const messageDiv = document.createElement("div");
  messageDiv.className = type;
  messageDiv.textContent = text;
  chatMessages.appendChild(messageDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}
async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;
  addMessage(message, "user");
  userInput.value = "";
  try {
    const response = await fetch("http://127.0.0.1:5000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });
    if (!response.ok) throw new Error("Network response was not ok");
    const data = await response.json();
    console.log("Backend Response:", data);
    addMessage(data.response, "bot");
  } catch (error) {
    console.error("Error:", error);
    addMessage("Oops! Something went wrong.", "bot");
  }
}
sendButton.addEventListener("click", sendMessage);
userInput.addEventListener("keypress", (event) => {
  if (event.key === "Enter") sendMessage();
});
