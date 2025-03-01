from googleapiclient.discovery import build
from authenticate import gmail_authenticate

def get_sent_emails(max_results=10):
    """Fetch sent emails from Gmail."""
    creds = gmail_authenticate()
    service = build("gmail", "v1", credentials=creds)

    results = service.users().messages().list(
        userId="me", labelIds=["SENT"], maxResults=max_results
    ).execute()
    
    messages = results.get("messages", [])

    if not messages:
        print("No sent emails found.")
        return []

    email_data = []
    for msg in messages:
        msg_details = service.users().messages().get(userId="me", id=msg["id"]).execute()
        email_data.append(msg_details)

    return email_data

if __name__ == "__main__":
    sent_emails = get_sent_emails(5)
    for email in sent_emails:
        print(email["snippet"])  # Print email preview
