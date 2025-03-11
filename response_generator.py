import os
from openai import OpenAI
from dotenv import load_dotenv
from vector_database import add_new_emails_to_faiss, retrieve_similar_emails
from fetch_sent_emails import get_clean_sent_emails
load_dotenv()


from vector_database import retrieve_similar_emails

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_email_response(query, compose_type="new"):
    # get_clean_sent_emails()
    add_new_emails_to_faiss()
    similar_emails = retrieve_similar_emails(query, top_k=3)
    context = "\n\n".join([f"Past Email {i+1}: {em}" for i, em in enumerate(similar_emails)])

    if compose_type == "reply":
        prompt = f"""
        You are an AI email assistant that writes replies in the user's style.

        The user is replying to an existing thread:
        {query}

        Here are relevant past emails from the user:
        {context}

        Please produce a well-written, context-aware reply that matches the user's typical style.
        """
        # print("Reply Prompt:", prompt)
    else:
        prompt = f"""
        You are an AI email assistant that writes new emails in the user's style.

        Email context:
        {query}

        Relevant Past Emails:
        {context}

        Please produce a well-written, personalized new email.
        """
        # print("New Email Prompt:", prompt)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a personal AI email assistant."},
                  {"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    add_new_emails_to_faiss() 
    test_query = "Regarding grading discussion"
    ai_resp = generate_email_response(test_query)
    print("\n📩 AI-Generated Email Response:")
    print(ai_resp)
