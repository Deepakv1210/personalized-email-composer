console.log("📩 Gmail AI Assistant Loaded!");

function addAIButton() {
    const composeToolbar = document.querySelector(".aoD.az6");

    if (composeToolbar && !document.getElementById("ai-suggest-button")) {
        let aiButton = document.createElement("button");
        aiButton.id = "ai-suggest-button";
        aiButton.innerText = "✨ AI Suggest";
        aiButton.style = "margin-left: 10px; padding: 5px; border-radius: 5px; background: #4285F4; color: white; cursor: pointer;";
        
        aiButton.onclick = async function () {
            let emailBody = document.querySelector(".Am.Al.editable").innerText;
            let subject = document.querySelector("input[name='subjectbox']").value;
            
            if (!emailBody.trim()) {
                alert("⚠️ Please type an email before requesting AI suggestions.");
                return;
            }

            console.log("📝 Sending email draft to AI...");
            let response = await fetch("http://localhost:5000/generate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ subject: subject, body: emailBody })
            });

            let data = await response.json();
            document.querySelector(".Am.Al.editable").innerText = data.suggestion;
        };

        composeToolbar.appendChild(aiButton);
        console.log("✨ AI Button Added!");
    }
}

setInterval(addAIButton, 2000); 
