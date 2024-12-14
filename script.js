// References to DOM elements
const chatMessages = document.getElementById("chatMessages");
const userInput = document.getElementById("userInput");
const sendButton = document.getElementById("sendButton");

// Add a new message to the chat window
function addMessage(text, type) {
  const messageDiv = document.createElement("div");
  messageDiv.className = type;
  messageDiv.textContent = text;
  chatMessages.appendChild(messageDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight; // Auto-scroll to the bottom
}

// Send message to the backend and display the response
async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;

  // Display the user's message
  addMessage(message, "user");
  userInput.value = "";

  try {
    // Send user input to the Flask backend
    const response = await fetch("http://127.0.0.1:5000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    if (!response.ok) throw new Error("Network response was not ok");

    const data = await response.json();
    // Display chatbot's response
    addMessage(data.response, "bot");
  } catch (error) {
    console.error("Error:", error);
    addMessage("Oops! Something went wrong.", "bot");
  }
}

// Event listener for the send button
sendButton.addEventListener("click", sendMessage);

// Send message on Enter key press
userInput.addEventListener("keypress", (event) => {
  if (event.key === "Enter") sendMessage();
});
