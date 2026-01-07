from sentence_transformers import SentenceTransformer
import chromadb
import json

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.Client()
collection = client.get_or_create_collection("website_data")

with open("pages.json", encoding="utf-8") as f:
    pages = json.load(f)

def index_website(pages_dict):
    if not pages_dict:
        return "No pages to index!"

    for i, (url, text) in enumerate(pages_dict.items()):
        emb = model.encode(text).tolist()
        collection.add(
            ids=[str(i)],
            documents=[text],
            metadatas=[{"url": url}],
            embeddings=[emb]
        )
    return "Indexing completed!"


if __name__ == "__main__":
    print(index_website(pages))
