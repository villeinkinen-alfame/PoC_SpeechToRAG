# Only imports search_db from store.py — no transcription model is loaded, so it starts instantly.
from store import search_db

query = "Mitä tarvitsen pulloraketin tekoon?" # "What do I need to build a bottle rocket?"
'''NOTE: Be wary of query language mismatch — "Mäkiauto"-example is in Finnish, but the bottle rocket content is in English.
ChromaDB's default embedding model uses semantic similarity where cross-language matching is weak!'''

results = search_db(query)

if results['documents']:
    print(f"Top Match Found:\n{results['documents'][0][0]}")
else:
    print("No relevant info found.")
