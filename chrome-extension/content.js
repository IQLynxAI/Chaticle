// Extracts the visible text from the webpage
function getPageContent() {
    return document.body.innerText;
}

// Listen for messages from popup.js
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "extract_content") {
        let content = getPageContent();
        sendResponse({ content: content });
    }
});
