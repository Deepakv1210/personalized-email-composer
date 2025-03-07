document.getElementById("fetch-suggestion").addEventListener("click", () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        chrome.tabs.sendMessage(tabs[0].id, { action: "fetch_ai_suggestion" }, (response) => {
            document.getElementById("output").innerText = response.suggestion || "⚠️ No response.";
        });
    });
});
