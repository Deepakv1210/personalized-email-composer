import re
import base64
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from authenticate import gmail_authenticate
from secure_storage import insert_email

def extract_text_from_parts(parts):
    """Recursively extract text content from email parts."""
    for part in parts:
        mime_type = part.get("mimeType", "")
        body = part.get("body", {})
        data = body.get("data", "")

        if mime_type == "text/plain" and data:
            return base64.urlsafe_b64decode(data).decode("utf-8").strip()

        elif mime_type == "text/html" and data:
            html_content = base64.urlsafe_b64decode(data).decode("utf-8")
            return BeautifulSoup(html_content, "html.parser").get_text(separator=" ").strip()

        elif "parts" in part:  # If nested, recurse deeper
            text = extract_text_from_parts(part["parts"])
            if text:
                return text

    return ""

def decode_email_body(payload):
    """Handles different email structures to extract the full body."""
    if "parts" in payload:  # Multipart email (most cases)
        return extract_text_from_parts(payload["parts"])
    
    elif "body" in payload and "data" in payload["body"]:  # Single-part email
        data = payload["body"]["data"]
        return base64.urlsafe_b64decode(data).decode("utf-8").strip()

    return ""

def extract_email_components(email_body):
    """Extracts greeting, body, and closing from an email body."""
    
    # Extract greeting (if present)
    greeting_regex = r"^(Hi|Hello|Dear|Hey)\s[\w\s,]+"
    greeting_match = re.search(greeting_regex, email_body, re.IGNORECASE)
    greeting = greeting_match.group(0) if greeting_match else None

    # Remove quoted replies (Gmail style)
    reply_cutoff = re.split(r"\nOn .* wrote:\n", email_body)
    latest_message = reply_cutoff[0].strip()

    # Extract closing (multi-line support)
    closing_regex = r"((Best|Regards|Sincerely|Thanks & Regards|Cheers|Looking forward to hearing from you)[,\n]?\s*\n?[^\n]+(?:\n[^\n]+)*)$"
    closing_match = re.search(closing_regex, latest_message, re.IGNORECASE)
    closing = closing_match.group(1).strip() if closing_match else None

    # Remove greeting & closing from main body
    email_body_cleaned = latest_message
    if greeting:
        email_body_cleaned = email_body_cleaned.replace(greeting, "").strip()
    if closing:
        email_body_cleaned = email_body_cleaned.replace(closing, "").strip()

    return {
        "greeting": greeting,
        "body": email_body_cleaned,
        "closing": closing
    }

def clean_greeting(greeting):
    """Ensures greeting contains only the first line after Hi/Hello/Dear."""
    if greeting:
        greeting = greeting.strip()
        greeting = greeting.split("\n")[0].strip()  # ✅ Stop at first line
        greeting = re.sub(r"[\r\n]+", " ", greeting)  # ✅ Remove any extra newlines
        return greeting
    return None

def clean_closing(closing):
    """Removes forwarded metadata from closing and ensures it's properly formatted."""
    if closing:
        closing = closing.strip()
        closing = re.sub(r"\nOn .* wrote:.*", "", closing, flags=re.DOTALL)  # ✅ Remove forwarded metadata
        closing = re.sub(r"[\r\n]+", " ", closing)  # ✅ Replace extra newlines with spaces
        return closing.strip()
    return None
def clean_email_body(email_text):
    """Removes signatures, disclaimers, and forwarded content."""
    
    # Remove quoted replies (common in Gmail)
    email_text = re.sub(r"(?m)^>.*\n?", "", email_text)
    
    # Remove signatures (if email contains '--' or 'Sent from my iPhone')
    email_text = re.split(r"--|Sent from my iPhone", email_text)[0]
    
    # Remove disclaimers (text starting with 'This email contains confidential information')
    email_text = re.sub(r"This email contains confidential information.*", "", email_text, flags=re.DOTALL)

    return email_text.strip()

def get_clean_sent_emails(max_results=10):
    """Fetch, preprocess, and store sent emails securely."""
    creds = gmail_authenticate()
    service = build("gmail", "v1", credentials=creds)

    results = service.users().messages().list(
        userId="me", labelIds=["SENT"], maxResults=max_results
    ).execute()
    
    messages = results.get("messages", [])

    if not messages:
        print("No sent emails found.")
        return []

    cleaned_emails = []
    for msg in messages:
        msg_details = service.users().messages().get(userId="me", id=msg["id"]).execute()

        # Extract subject from headers
        payload = msg_details.get("payload", {})
        headers = payload.get("headers", [])
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject")

        # Decode and clean email body
        email_body = decode_email_body(payload)
        structured_email = extract_email_components(email_body)

        # ✅ Fix Greeting & Closing Before Storing
        structured_email["greeting"] = clean_greeting(structured_email["greeting"])
        structured_email["closing"] = clean_closing(structured_email["closing"])

        # Store structured email securely
        insert_email(subject, structured_email["greeting"], structured_email["body"], structured_email["closing"])

        # Append to in-memory list
        cleaned_emails.append({
            "subject": subject,
            "greeting": structured_email["greeting"],
            "body": structured_email["body"],
            "closing": structured_email["closing"]
        })

    return cleaned_emails

# def get_clean_sent_emails(max_results=10):
#     """Fetch, preprocess, and store sent emails securely."""
#     creds = gmail_authenticate()
#     service = build("gmail", "v1", credentials=creds)

#     results = service.users().messages().list(
#         userId="me", labelIds=["SENT"], maxResults=max_results
#     ).execute()
    
#     messages = results.get("messages", [])

#     if not messages:
#         print("No sent emails found.")
#         return []

#     cleaned_emails = []
#     for msg in messages:
#         msg_details = service.users().messages().get(userId="me", id=msg["id"]).execute()

#         # Extract subject from headers
#         payload = msg_details.get("payload", {})
#         headers = payload.get("headers", [])
#         subject = next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject")

#         # Decode and clean email body
#         email_body = decode_email_body(payload)
#         email_body = clean_email_body(email_body)
#         structured_email = extract_email_components(email_body)

#         # Store structured email securely
#         insert_email(subject, structured_email["greeting"], structured_email["body"], structured_email["closing"])

#         # Append to in-memory list
#         cleaned_emails.append({
#             "subject": subject,
#             "greeting": structured_email["greeting"],
#             "body": structured_email["body"],
#             "closing": structured_email["closing"]
#         })

#     return cleaned_emails

if __name__ == "__main__":
    sent_emails = get_clean_sent_emails(5)
    print("\nStored Emails in Secure DB ✅")


