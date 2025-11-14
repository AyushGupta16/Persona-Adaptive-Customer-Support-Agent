import os
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

CHROMA_DIR = "./chroma_db"
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory=CHROMA_DIR))
COLLECTION_NAME = "supportkb"

def load_kb(kb_folder: str = "knowledge_base"):
    if COLLECTION_NAME in [c.name for c in client.list_collections()]:
        collection = client.get_collection(COLLECTION_NAME)
    else:
        collection = client.create_collection(name=COLLECTION_NAME, metadata={})

    # Ingest KB if empty
    if collection.count() == 0:
        docs, metadatas, ids = [], [], []
        for fname in os.listdir(kb_folder):
            path = os.path.join(kb_folder, fname)
            if os.path.isfile(path):
                with open(path, "r", encoding="utf-8") as f:
                    text = f.read().strip()
                docs.append(text)
                metadatas.append({"source": fname})
                ids.append(fname)
        if docs:
            collection.add(documents=docs, metadatas=metadatas, ids=ids)
            client.persist()
    return client.get_collection(COLLECTION_NAME)

def retrieve_docs(query: str, collection, k: int = 2):
    emb = embed_model.encode(query).tolist()
    results = collection.query(query_embeddings=[emb], n_results=k)
    docs = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    return docs, metadatas
