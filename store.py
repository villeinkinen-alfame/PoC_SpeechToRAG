import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter # used for chunking long documents
from collections import defaultdict
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

COLLECTION_NAME = "expert_knowledge_multilingual"   # A single collection can hold all experts' knowledge, with metadata to differentiate them.
EMBEDDING_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2" # A multilingual model that can handle Finnish and English reasonably well.

# Initialize the database (a local folder named 'gasket_knowledge_db')
client = chromadb.PersistentClient(path="./gasket_knowledge_db")
embedding_function = SentenceTransformerEmbeddingFunction(
    model_name=EMBEDDING_MODEL_NAME
)
collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_function,
)

# Initialize the chunk splitter. Adjust chunk_size and chunk_overlap based on typical document lengths and desired context retention.
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,         # Character count per chunk. Smaller size = Each retrieved result is more directly relevant to the query (less noise).
    chunk_overlap=100,      # Keeps context between chunks, ESPECIALLY when small(er) chunk sizes are used.
    separators=["\n\n", "\n", ".", " ", ""] # Split order
)

def save_to_db(full_text, metadata):
    # 1. Chunk the text
    chunks = text_splitter.split_text(full_text)
    
    documents = []
    metadatas = []
    ids = []
    
    # 2. Prepare lists for each chunk
    for i, chunk in enumerate(chunks):
        documents.append(chunk)
        
        # Merge existing metadata with chunk-specific info
        chunk_metadata = metadata.copy()
        chunk_metadata["chunk_index"] = i
        metadatas.append(chunk_metadata)
        
        # Create a unique ID for every chunk (timestamp + index)
        ids.append(f"{metadata['expert']}_{int(metadata['timestamp'])}_{i}")

    # 3. Add the list of chunks to ChromaDB
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    print(f"Successfully stored {len(chunks)} chunks in the database.")

def search_db(query):
    # n_results=3 is better once you have chunks, to get a fuller answer
    results = collection.query(query_texts=[query], n_results=3)
    return results


def reset_collection():
    # Delete and recreate the active collection with the configured embedding model.
    global collection
    client.delete_collection(name=COLLECTION_NAME)
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_function,
    )
    return {"collection_name": COLLECTION_NAME, "remaining_count": collection.count()}

# Utility to clean up duplicates or stale entries in the database
def cleanup_duplicates(remove_unknown=True, keep_latest_per_source=True):
    """Clean stale and duplicate entries from the Chroma collection.

    Rules:
    - Optionally remove entries with missing source_file metadata ("unknown").
    - Optionally keep only the newest ingestion per source_file based on timestamp.
    """
    all_items = collection.get(include=["metadatas"])
    ids = all_items.get("ids", [])
    metadatas = all_items.get("metadatas", [])

    grouped = defaultdict(list)
    for item_id, meta in zip(ids, metadatas):
        src = meta.get("source_file", "unknown") if meta else "unknown"
        ts = meta.get("timestamp", 0) if meta else 0
        grouped[src].append((ts, item_id))

    ids_to_delete = []

    for src, entries in grouped.items():
        if remove_unknown and src == "unknown":
            ids_to_delete.extend([item_id for _, item_id in entries])
            continue

        if keep_latest_per_source:
            timestamps = sorted(set(ts for ts, _ in entries), reverse=True)
            if len(timestamps) > 1:
                latest_ts = timestamps[0]
                ids_to_delete.extend(
                    [item_id for ts, item_id in entries if ts != latest_ts]
                )

    if ids_to_delete:
        collection.delete(ids=ids_to_delete)

    return {
        "deleted_count": len(ids_to_delete),
        "remaining_count": collection.count(),
        "deleted_ids": ids_to_delete,
    }
