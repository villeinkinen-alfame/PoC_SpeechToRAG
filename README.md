# PoC_SpeechToRAG
Python based MVP on how to implement speech to text, chunking/saving to vectorDB and retrieval of relevant data when asked

Get an audio file (mp3 or mp4 both work) with speech you want to query:
1) Transcribe transforms audio to text
2) Store chunks the text and stores it into a local ChromaDB (also cleans stale and duplicate entires)
3) Main is the actual executable to call other parts and is where i.e. the audio file is hard coded atm.
4) Query provides a way to retrieve data from the DB

To do:
-Socratic interviewer AI for knowledge “extraction” and Q&A automation
-Chunk size adjusting for more accurate answers/retrieval
-Creating answers using LLM+RAG from the company knowledge DB => “Natural” language & “filling” around the tech.
