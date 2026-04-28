# PoC_SpeechToRAG (https://docs.google.com/document/d/1WUx3HAGbyoxDPp6t4jNkyjC8pN1pD5po5Z6P4bU3ePs/edit?usp=sharing)
Python based MVP on how to implement speech to text, chunking/saving to vectorDB and retrieval of relevant data when asked. Should have at least 5GB free RAM in the environment, ffmpeg installed on the system to handle the audio and a python environment with gasket-ai-local, faster-whisper, chromadb, sentence-transformers & langchain-text-splitters (not sure if forgetting something).

Prep in powershell:
1) mkdir gasket-ai-local
2) cd gasket-ai-local
3) python -m venv venv
Note: Should have VS Code and Python here for easy continuation
4) venv\Scripts\activate
5) pip install faster-whisper chromadb sentence-transformers
6) pip install langchain-text-splitters


Get an audio file (mp3 or mp4 both work) with speech you want to query:
1) Transcribe transforms audio to text
2) Store chunks the text and stores it into a local ChromaDB (also cleans stale and duplicate entires)
3) Main is the actual executable to call other parts and is where i.e. the audio file is hard coded atm.
4) Query provides a way to retrieve data from the DB

To do (random order):
1) Socratic interviewer AI for knowledge “extraction” from expert and Q&A automation
2) Chunk size adjusting for more accurate answers/retrieval based on the use case
3) Creating answers using LLM+RAG from the company knowledge DB => “Natural” language & “filling” around the tech.
