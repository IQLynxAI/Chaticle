document.addEventListener("DOMContentLoaded", () => {
    // Auto-extract content when extension opens
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        chrome.scripting.executeScript(
            {
                target: { tabId: tabs[0].id },
                function: extractAndSendContent
            }
        );
    });

    // Handle clicking the "Send" button
    document.getElementById("ask-question").addEventListener("click", sendMessage);

    // Handle "Enter" key press in input field
    document.getElementById("question").addEventListener("keypress", function (event) {
        if (event.key === "Enter") {  // Check if Enter was pressed
            event.preventDefault();  // Prevent default form submission
            sendMessage();  // Call sendMessage function
        }
    });
});

// Function to extract content and send to backend
function extractAndSendContent() {
    let content = document.body.innerText;

    fetch("http://127.0.0.1:8000/store_content", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content: content })
    }).then(response => response.json())
      .then(data => console.log("Content sent:", data))
      .catch(error => console.error("Error:", error));
}

// Function to send a message (Used by both button & "Enter" key)
function sendMessage() {
    let questionInput = document.getElementById("question");
    let question = questionInput.value.trim();
    if (question === "") return;

    addMessage("user", question);  // Show user's message in UI

    fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: question })
    }).then(response => response.json())
      .then(data => {
          addMessage("bot", data.answer);  // Show AI response in UI
      })
      .catch(error => console.error("Error:", error));

    questionInput.value = "";  // Clear input field
}

// Function to add chat messages to UI
function addMessage(type, text) {
    let chatBox = document.getElementById("chat-box");
    let message = document.createElement("div");
    message.classList.add("message", type);
    message.innerText = text;
    chatBox.appendChild(message);

    // Auto-scroll to the latest message
    chatBox.scrollTop = chatBox.scrollHeight;
}
