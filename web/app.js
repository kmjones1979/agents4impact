// API Base URLs
const API_URLS = {
    orchestrator: "http://localhost:8000",
    bigquery: "http://localhost:8001",
    ticket: "http://localhost:8002",
    maps: "http://localhost:8003",
};

// Initialize app
document.addEventListener("DOMContentLoaded", () => {
    checkAgentStatus();
    setupEventListeners();

    // Refresh agent status every 10 seconds
    setInterval(checkAgentStatus, 10000);
});

// Check if all agents are running
async function checkAgentStatus() {
    for (const [name, url] of Object.entries(API_URLS)) {
        const statusElement = document.getElementById(`status-${name}`);
        if (!statusElement) continue;

        try {
            const response = await fetch(`${url}/health`, { 
                signal: AbortSignal.timeout(5000) 
            });
            
            if (response.ok) {
                statusElement.classList.add("online");
                statusElement.classList.remove("offline");
                statusElement.querySelector(".status-text").textContent = "Online";
            } else {
                throw new Error("Not healthy");
            }
        } catch (error) {
            statusElement.classList.add("offline");
            statusElement.classList.remove("online");
            statusElement.querySelector(".status-text").textContent = "Offline";
        }
    }
}

// Setup event listeners
function setupEventListeners() {
    // Bottom navigation
    document.querySelectorAll(".nav-button").forEach((button) => {
        button.addEventListener("click", () => {
            const viewName = button.dataset.view;
            switchView(viewName);
        });
    });

    // Chat
    document.getElementById("send-button").addEventListener("click", sendChatMessage);
    document.getElementById("chat-input").addEventListener("keypress", (e) => {
        if (e.key === "Enter") sendChatMessage();
    });
}

// Switch between views
function switchView(viewName) {
    // Update navigation buttons
    document.querySelectorAll(".nav-button").forEach((btn) => {
        btn.classList.remove("active");
    });
    document.querySelector(`[data-view="${viewName}"]`).classList.add("active");

    // Update views
    document.querySelectorAll(".view").forEach((view) => {
        view.classList.remove("active");
    });
    document.getElementById(`${viewName}-view`).classList.add("active");
}

// Chat functionality
async function sendChatMessage() {
    const input = document.getElementById("chat-input");
    const message = input.value.trim();

    if (!message) return;

    // Add user message to chat
    addMessage("user", message);
    input.value = "";

    // Show loading
    const loadingId = addMessage("assistant", '<div class="loading">Thinking</div>');

    try {
        // Send message to orchestrator
        const response = await fetch(`${API_URLS.orchestrator}/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: message }),
        });

        const data = await response.json();

        // Remove loading message
        document.querySelector(`[data-message-id="${loadingId}"]`)?.remove();

        if (data.success) {
            let responseText = data.response || "No response received.";
            addMessage("assistant", responseText);
        } else {
            addMessage("error", data.error || "Sorry, I encountered an error. Please try again.");
        }
    } catch (error) {
        document.querySelector(`[data-message-id="${loadingId}"]`)?.remove();
        addMessage("error", `Error: ${error.message}`);
    }
}

function addMessage(type, content) {
    const messagesContainer = document.getElementById("chat-messages");
    const messageId = Date.now();
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${type}`;
    messageDiv.dataset.messageId = messageId;

    const bubble = document.createElement("div");
    bubble.className = "message-bubble";

    const messageContent = document.createElement("div");
    messageContent.className = "message-content";
    messageContent.innerHTML = content.replace(/\n/g, "<br>");

    bubble.appendChild(messageContent);
    messageDiv.appendChild(bubble);
    messagesContainer.appendChild(messageDiv);

    // Scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    return messageId;
}
