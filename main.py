# takes an audio file, transcribes it, and saves it to 'store' chroma-database
import time
from transcribe import get_transcription
from store import save_to_db, search_db

# 1. Transcribe the audio
audio_file = "bottle_rocket.mp3" # Audio file in case ('makiauto.mp4', 'bottle_rocket.mp3')
print(f"Starting transcription for {audio_file}...")
transcribed_text, detected_language = get_transcription(audio_file)

# 2. Store in the database
print("Saving to local DB...")
# Pass the metadata dictionary; the store function handles the IDs
save_to_db(transcribed_text, {
    "expert": "Ville",  # Jari for actual expert, Ville as tester
    "timestamp": time.time(),
    "source_file": audio_file,
    "language": detected_language
})

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