import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from secure_storage import fetch_all_emails 

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cuda")
D = 384  
index = faiss.IndexFlatIP(D)  
email_lookup = {} 

def load_embeddings():
    """Load saved FAISS embeddings + email_lookup if they exist."""
    emb_path = "email_embeddings.npy"
    lookup_path = "email_lookup.npy"
    if os.path.exists(emb_path) and os.path.exists(lookup_path):
        index.reset()  
        embeddings = np.load(emb_path)
        index.add(embeddings)
        print(f"✅ Loaded {index.ntotal} embeddings into FAISS from {emb_path}.")

        global email_lookup
        email_lookup = np.load(lookup_path, allow_pickle=True).item()
        print(f"✅ email_lookup loaded with {len(email_lookup)} entries.")
    else:
        print("⚠️ No saved FAISS data found. Starting empty index.")

def save_embeddings():
    """Re-extract all from FAISS and save them + email_lookup."""
    if index.ntotal > 0:
        # Reconstruct all vectors from index
        all_vecs = index.reconstruct_n(0, index.ntotal)
        np.save("email_embeddings.npy", all_vecs)
        np.save("email_lookup.npy", email_lookup)
        print(f"✅ Saved {index.ntotal} embeddings + {len(email_lookup)} in email_lookup.")
    else:
        print("⚠️ Index is empty; nothing to save.")

def add_new_emails_to_faiss():
    """
    1) Load existing data (if not loaded yet)
    2) Retrieve emails from DB
    3) Embed + add only those not in email_lookup
    4) Save updated state
    """
    if index.ntotal == 0 and not email_lookup:
        load_embeddings() 

    emails = fetch_all_emails()  # from SQLite
    if not emails:
        print("⚠️ No emails found in DB.")
        return

    new_texts = []
    start_count = len(email_lookup)
    for idx, (subject, greeting, body, closing) in enumerate(emails):
        if idx in email_lookup:
            continue  # Already indexed
        full_text = f"{subject} {greeting} {body} {closing}"
        email_lookup[idx] = full_text
        new_texts.append(full_text)

    if not new_texts:
        print("✅ No new emails to index. Up to date.")
        return

    # Encode only new emails
    new_embeddings = model.encode(new_texts, convert_to_numpy=True)
    faiss.normalize_L2(new_embeddings)

    # Add them to FAISS
    index.add(new_embeddings)

    # Save updated data
    save_embeddings()
    added_count = len(email_lookup) - start_count
    print(f"✅ Indexed {added_count} new emails in FAISS.")

def retrieve_similar_emails(query, top_k=3):
    """Search FAISS for top-k most similar emails."""
    if index.ntotal == 0:
        print("⚠️ FAISS is empty, no emails to retrieve.")
        return []

    query_emb = model.encode([query], convert_to_numpy=True)
    faiss.normalize_L2(query_emb)
    distances, indices = index.search(query_emb, top_k)

    print("\n🔍 Indices:", indices[0])
    print("🔍 Distances:", distances[0])
    print("🔍 email_lookup keys:", list(email_lookup.keys()))

    results = []
    for i in indices[0]:
        if i in email_lookup:
            results.append(email_lookup[i])
        else:
            print(f"⚠️ Index {i} not found in email_lookup.")
    return results

if __name__ == "__main__":
    add_new_emails_to_faiss() 
    query = "Meeting about CSCE 638 grader discussion"
    hits = retrieve_similar_emails(query)
    print("\nTop Similar Emails:")
    for h in hits:
        print("- ", h[:100], "...\n")
