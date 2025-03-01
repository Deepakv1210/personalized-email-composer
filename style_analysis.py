import nltk
import re
from textblob import TextBlob
from secure_storage import fetch_all_emails  # Fetch stored emails

# Ensure required NLTK resources are available
nltk.download('punkt')

def analyze_writing_style():
    """Analyzes user's writing style using previously stored greetings and closings."""
    emails = fetch_all_emails()
    
    style_data = {
        "greetings": {},
        "closings": {},
        "avg_sentence_length": 0,
        "formality": {"formal": 0, "casual": 0},
        "emoji_usage": 0
    }
    
    total_sentences = 0
    total_words = 0
    total_emails = len(emails)

    for email in emails:
        subject, greeting, body, closing = email  # ✅ Use stored values directly

        # **Ensure Greetings and Closings Are Stored Correctly**
        if greeting and greeting != "None":
            style_data["greetings"][greeting] = style_data["greetings"].get(greeting, 0) + 1
        
        if closing and closing != "None":
            style_data["closings"][closing] = style_data["closings"].get(closing, 0) + 1

        # **Sentence Length Analysis**
        sentences = nltk.sent_tokenize(body)
        total_sentences += len(sentences)
        total_words += len(body.split())

        # **Improved Formality Analysis**
        if closing and any(word in closing.lower() for word in ["regards", "sincerely", "best", "dear", "yours truly"]):
            style_data["formality"]["formal"] += 1
        else:
            style_data["formality"]["casual"] += 1

        # **Count Emoji Usage**
        style_data["emoji_usage"] += len(re.findall(r"[😊😂👍🙌❤️🔥🙏💡🤔💪]", body))

    # **Calculate Averages**
    if total_sentences > 0:
        style_data["avg_sentence_length"] = total_words / total_sentences

    return style_data

if __name__ == "__main__":
    style_profile = analyze_writing_style()
    print("\n📌 Writing Style Analysis:")
    print("Common Greetings:", style_profile["greetings"])
    print("Common Closings:", style_profile["closings"])
    print("Average Sentence Length:", round(style_profile["avg_sentence_length"], 2))
    print("Formality Ratio:", style_profile["formality"])
    print("Emoji Usage Count:", style_profile["emoji_usage"])

# if __name__ == "__main__":
#     emails = fetch_all_emails()

#     print("\n🔍 DEBUG: Emails in Database")
#     for idx, email in enumerate(emails):
#         subject, greeting, body, closing = email
#         print(f"\n--- Email {idx+1} ---")
#         print(f"Subject: {subject}")
#         print(f"Greeting: {greeting}")
#         print(f"Body:\n{body}...")  # Print only the first 100 chars for preview
#         print(f"Closing: {closing}")
#         print("-" * 10)
