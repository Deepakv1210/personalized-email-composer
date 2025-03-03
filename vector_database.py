import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from secure_storage import fetch_all_emails  # Fetch stored emails
import os

# Save embeddings after first indexing
def save_embeddings():
    np.save("email_embeddings.npy", index.reconstruct_n(0, index.ntotal))
    print("✅ Saved embeddings for faster retrieval.")

def load_embeddings():
    if os.path.exists("email_embeddings.npy"):
        global index
        embeddings = np.load("email_embeddings.npy")
        index.add(embeddings)
        print("✅ Loaded saved embeddings.")

# Load the embedding model
# model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cuda")

# FAISS index for Cosine Similarity (Use Inner Product, then normalize)
D = 384  # Embedding size for MiniLM
index = faiss.IndexFlatIP(D)  # Inner Product (Cosine requires normalization)

# Dictionary to map index IDs to email content
email_lookup = {}

def build_vector_database():
    """Embeds past emails and stores them in FAISS for retrieval using Cosine Similarity."""
    global email_lookup
    emails = fetch_all_emails()

    if os.path.exists("email_embeddings.npy"):
        load_embeddings()
        return

    email_texts = []
    for idx, (subject, greeting, body, closing) in enumerate(emails):
        full_text = f"{subject} {greeting} {body} {closing}"
        email_texts.append(full_text)
        email_lookup[idx] = full_text  # Store original text mapping

    embeddings = model.encode(email_texts, convert_to_numpy=True)
    faiss.normalize_L2(embeddings)  # Normalize for Cosine Similarity
    index.add(embeddings)
    
    save_embeddings()
    print(f"✅ Indexed {len(email_texts)} emails in vector database.")


def retrieve_similar_emails(query, top_k=3):
    """Finds past emails most similar to the current query using Cosine Similarity."""
    query_embedding = model.encode([query], convert_to_numpy=True)

    # 🔹 Normalize query embedding
    faiss.normalize_L2(query_embedding)

    # Search in FAISS
    D, I = index.search(query_embedding, top_k)

    # Retrieve top-k similar emails
    similar_emails = [email_lookup[i] for i in I[0] if i >= 0]
    return similar_emails


# Run this to build the database on startup
if __name__ == "__main__":
    build_vector_database()
    query = "Meeting about CSCE 638 grader discussion"
    retrieved_emails = retrieve_similar_emails(query)

    print("\n🔍 Top Similar Emails Retrieved:")
    for email in retrieved_emails:
        print(f"- {email}...\n") 
