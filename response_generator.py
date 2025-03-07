import os
from openai import OpenAI
from dotenv import load_dotenv
from vector_database import add_new_emails_to_faiss, retrieve_similar_emails
from fetch_sent_emails import get_clean_sent_emails
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_email_response(query):
    get_clean_sent_emails()
    add_new_emails_to_faiss()
    similar_emails = retrieve_similar_emails(query, top_k=3)
    if not similar_emails:
        return "No past emails retrieved - possibly empty FAISS"
    context = "\n\n".join(
        f"Past Email {i+1}: {email}" for i, email in enumerate(similar_emails)
    )
    print("Context:", context)
    prompt = f"""
    You are an AI email assistant that writes responses in the user's style.
    
    **Current Email Query:**
    "{query}"
    
    **Relevant Past Emails:**
    {context}

    Based on these past emails, generate a well-written, personalized response:
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a personal AI email assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    test_query = "Thank you for the interview update"
    ai_resp = generate_email_response(test_query)
    print("\n📩 AI-Generated Email Response:")
    print(ai_resp)
