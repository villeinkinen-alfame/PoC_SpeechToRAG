# takes an audio file, transcribes it, and saves it to 'store' chroma-database
import time
from transcribe import get_transcription
from store import save_to_db, search_db
from validate import prepare_text_for_db

def ingest_audio_to_db(audio_file, expert="Jari"):
    # 1. Transcribe the audio
    print(f"Starting transcription for {audio_file}...")
    raw_data, detected_language = get_transcription(audio_file)

    # 1.5 Clean and validate the transcript before saving it to the database.
    ready_for_db = prepare_text_for_db(raw_data, lang=detected_language)

    # 2. Store in the database
    print("Saving to local DB...")
    save_to_db(ready_for_db, {
        "expert": expert,  # Jari for actual expert
        "timestamp": time.time(),
        "source_file": audio_file,
        "language": detected_language,
        "raw_data": raw_data,
        "validated": ready_for_db != raw_data,
    })

    return {
        "audio_file": audio_file,
        "language": detected_language,
        "raw_data": raw_data,
        "ready_for_db": ready_for_db,
    }


if __name__ == "__main__":
    audio_file = "cuttingprocesses_long.mp3"  # Audio file in case ('makiauto.mp4', 'bottle_rocket.mp3', 'cuttingprocesses_long.mp3')
    result = ingest_audio_to_db(audio_file)
    print(f"Detected language: {result['language']}")
    print(f"Stored text preview: {result['ready_for_db'][:200]}")

'''
# 3. Test Retrieval
print("\n--- Testing Retrieval ---")
query = "Tarvitaanko pyöränpumppu pulloraketin rakentamiseen?"  # Adjust this query based on the actual content of the audio
results = search_db(query)
# Select best of three results (defined in store.py)
if results['documents']:
    print(f"Top Match Found:\n{results['documents'][0][0]}") 
else:
    print("No relevant info found.")
'''
