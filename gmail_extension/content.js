console.log("📩 Gmail AI Assistant Loaded!");
setInterval(() => {
    injectAIButton();
}, 2000);

function injectAIButton() {
    // classes vary depending on new/reply
    const toolbars = document.querySelectorAll(".aoD.az6, .aoD.aZ6, .aDh");
  
    toolbars.forEach((toolbar) => {
      if (!toolbar.querySelector("#ai-suggest-button")) {
        let aiButton = document.createElement("button");
        aiButton.id = "ai-suggest-button";
        aiButton.innerText = "✨ AI Suggest";
        aiButton.style = "margin-left: 10px; ... your styling ...";
  
        aiButton.onclick = handleAIRequest;
        toolbar.appendChild(aiButton);
  
        console.log("✨ AI Button Added inside compose toolbar!", toolbar);
      }
    });
  }

function detectComposeType() {
    let subjectText = document.querySelector("input[name='subjectbox']")?.value || "";
    let bodyText = document.querySelector(".Am.Al.editable")?.innerText || "";
    if (subjectText.startsWith("Re:") || bodyText.includes("On ") || bodyText.includes("wrote:")) {
        return "reply";
    }
    return "new";
}

async function handleAIRequest() {
    let subjectInput = document.querySelector("input[name='subjectbox']");
    if (!subjectInput) {
      console.warn("No subject box found! Possibly a reply scenario. We'll use a fallback subject.");
    }
  
    // reading the subject if it's defined
    let subject = subjectInput ? subjectInput.value : "(No Subject)";
  
    // check for the body
    let bodyElem = document.querySelector(".Am.Al.editable");
    if (!bodyElem) {
      console.warn("No compose body found! Possibly the user hasn't opened the compose fully?");
      return;
    }
    let emailBody = bodyElem.innerText;
    let postData = {
      subject: subject,
      body: emailBody,
      composeType: detectComposeType()
    };
    console.log("📝 Sending data to AI server:", postData);

    let response = await fetch("http://localhost:5000/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(postData)
    });

    let data = await response.json();
    console.log("AI server responded with:", data);

    // insert AI suggestion
    let editable = document.querySelector(".Am.Al.editable");
    if (editable && data.suggestion) {
        editable.innerText = data.suggestion;
    }
}
  