chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "fetch_ai_suggestion") {
        fetch("http://localhost:5000/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ subject: message.subject, body: message.body })
        })
        .then(response => response.json())
        .then(data => sendResponse({ suggestion: data.suggestion }))
        .catch(error => sendResponse({ error: error.message }));

        return true;
    }
});
