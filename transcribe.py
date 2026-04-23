from faster_whisper import WhisperModel

# Use 'small' for speed, 'large-v3' for best Finnish accuracy. "turbo" for a fine-tuned version of large-v3 that has been pruned (from 32 layers down to 4) making it roughly 8x faster
model_size = "large-v3"     # large-v3 for best Finnish accuracy
model = WhisperModel(model_size, device="cpu", compute_type="int8")

def get_transcription(audio_path):
    # 'task="translate"' will turn Finnish speech into English text automatically
    segments, info = model.transcribe(audio_path, beam_size=5)
    
    full_text = ""
    for segment in segments:
        full_text += segment.text + " "
    return full_text.strip(), info.language

'''
# Testing the transcription function with an audio file
 text = get_transcription("makiauto.mp4")    # bottle_rocket.mp3
 print(text)
'''