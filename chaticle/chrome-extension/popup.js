document.addEventListener("DOMContentLoaded", () => {
    // Auto-extract content when extension opens
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        if (tabs.length > 0) {
            chrome.scripting.executeScript(
                {
                    target: { tabId: tabs[0].id },
                    function: extractAndSendContent
                },
                () => {
                    // Optional: Handle any errors or post-execution logic
                    if (chrome.runtime.lastError) {
                        console.error("Error executing script:", chrome.runtime.lastError);
                    } else {
                        console.log("Content extraction script executed successfully.");
                    }
                }
            );
        } else {
            console.error("No active tab found.");
        }
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

    // Check if the text contains HTML code blocks
    if (text.includes('<pre><code>')) {
        // Create a container for the code block and copy button
        let codeContainer = document.createElement("div");
        codeContainer.classList.add("code-container");

        // Add the code block
        codeContainer.innerHTML = text;

        // Add a copy button
        let copyButton = document.createElement("button");
        copyButton.innerText = "Copy";
        copyButton.classList.add("copy-button");
        copyButton.addEventListener("click", () => {
            let code = codeContainer.querySelector("code").innerText;
            navigator.clipboard.writeText(code).then(() => {
                // Update button text and style
                copyButton.innerText = "Copied!";
                copyButton.classList.add("copied");
                setTimeout(() => {
                    copyButton.innerText = "Copy";
                    copyButton.classList.remove("copied");
                }, 2000);  // Reset button after 2 seconds
            }).catch(err => {
                console.error("Failed to copy code:", err);
            });
        });

        // Append the copy button to the code container
        codeContainer.appendChild(copyButton);

        // Append the code container to the message
        message.appendChild(codeContainer);
    } else {
        message.innerText = text;  // Render as plain text
    }

    chatBox.appendChild(message);

    // Auto-scroll to the latest message
    chatBox.scrollTop = chatBox.scrollHeight;
}