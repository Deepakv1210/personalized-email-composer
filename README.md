# Personalized Gmail Assistant

## 📌 Overview
This project is a **Gmail AI Assistant** that enhances email composition and replies using AI-powered suggestions. The assistant integrates directly into Gmail via a **browser extension**, analyzing the user's past emails to generate **context-aware** and **personalized** responses.

## 🚀 Features Implemented So Far
### ✅ **Gmail API Integration**
- Successfully integrated Gmail API for **OAuth authentication**.
- Retrieved user’s email metadata securely.

### ✅ **Personalized Writing Style using RAG**
- Utilizes **FAISS (Facebook AI Similarity Search)** for retrieving relevant past emails.
- An **AI Suggest button** in Gmail where it generates responses **matching the user’s tone and writing style**.
- Implemented **Retrieval-Augmented Generation (RAG)** for better contextual responses.

### ✅ **Browser Extension Implementation**
- Integrated AI functionality directly into **Gmail's UI** for seamless user experience.

## 🔧 Installation & Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/gmail-ai-assistant.git
   cd gmail-ai-assistant
  
2. Install Dependencies
   ```bash
   pip install -r requirements.txt
   npm install
   
3. Set Up Gmail API Credentials
    Go to the Google Cloud Console → create or select a project.
    Enable the Gmail API.
    Create OAuth 2.0 credentials (Client ID & secret).
    Place these credentials (JSON or client ID/secret) in your local config (.env file)
   
5. Run the Local AI Server
   ```bash
   python server.py
   
6. Load the Chrome Extension
    Open Chrome and navigate to chrome://extensions/
    Enable Developer Mode (top right)
    Click Load Unpacked
    Select the gmail_extension/ folder from this repo
   
## 🏃 Usage
1. **Open Gmail** in Chrome.
2. Click **Compose** or open a **reply**.
3. After a short delay, an **AI Suggest** button will appear in the toolbar.
4. **Click** the button to send your subject/body to the AI server.
5. The AI’s suggested text will overwrite your draft in Gmail.

---

## 🛠️ Next Steps
- **Transition** from RAG-only to a **hybrid RAG + fine-tuning** approach for deeper personalization.
- **Optimize performance** & reduce latency for email suggestions.
- **Real-time autocomplete implementation** while typing.
- **Ensure privacy** & security compliance (encrypt or anonymize user data, follow Gmail API policies).

---

## 💡 Contributing
1. Fork this repository  
2. Create a new branch for your feature/fix  
3. Commit & push your changes  
4. Open a Pull Request  

All contributions are welcome — feel free to add new features, improve the UI or fix bugs.

---

### 👤 Maintainer
[Deepak]([https://github.com/Deepakv1210])
