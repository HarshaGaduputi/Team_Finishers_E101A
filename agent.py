from sentence_transformers import SentenceTransformer
import chromadb
import json
import numpy as np
from playwright.sync_api import sync_playwright

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.Client()
collection = client.get_or_create_collection("website_data")

with open("site_map.json", encoding="utf-8") as f:
    site_map = json.load(f)

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9))

def answer_query(query):
    q_emb = model.encode(query).tolist()
    best_score = 0.0
    best_url = None
    best_text = None

    data = collection.get(include=["documents", "metadatas", "embeddings"])
    if not data["documents"]:
        return 0.0, None, "No indexed content available."

    for doc, meta, emb in zip(data["documents"], data["metadatas"], data["embeddings"]):
        score = cosine_similarity(q_emb, emb)
        if score > best_score:
            best_score = score
            best_url = meta.get("url")
            best_text = doc

    return best_score, best_url, best_text

def auto_navigate_to(url):
    reasoning_steps = []
    reasoning_steps.append("Step 1: Received navigation request")
    reasoning_steps.append("Step 2: Confidence score is high → auto navigation allowed")
    reasoning_steps.append("Step 3: Launching browser using Playwright")
    reasoning_steps.append(f"Step 4: Navigating to {url}")

    print("\n--- AI Agent Reasoning Phase ---")
    for step in reasoning_steps:
        print(step)
    print("--------------------------------\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)
        time.sleep(2)
        print("Navigation completed in browser!")

if __name__ == "__main__":
    print("\nAI Agent Ready!\n")
    while True:
        q = input("Ask a question (or 'exit'): ")
        if q.lower() == "exit":
            print("Bye!")
            break
        score, url, text = answer_query(q)
        print("Confidence:", round(score, 2))
        print("Best matched page:", url)

        if url and score > 0.75:
            print("Auto navigating now…")
            auto_navigate_to(url)
        else:
            print("Guiding user instead (confidence too low or page not found).")
        print("Answer from site:\n", text[:400], "\n---\n")
