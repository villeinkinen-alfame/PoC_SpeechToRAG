import re

try:
    import language_tool_python
except ModuleNotFoundError:
    language_tool_python = None

class TextSanitizer:
    def __init__(self):
        self._tools = {}

    def pre_clean(self, text):
        """Removes transcription 'junk' before checking grammar."""
        # Remove filler words (Finnish & English)
        fillers = r'\b(tota|niinku|vähä|no|umm|uh|err|like|you know)\b'
        text = re.sub(fillers, '', text, flags=re.IGNORECASE)
        # Remove transcription tags like [noise] or [silence]
        text = re.sub(r'\[.*?\]', '', text)
        # Normalize spaces and punctuation left behind by filler removal.
        text = " ".join(text.split())
        text = re.sub(r'\s+([,.;:!?])', r'\1', text)
        text = re.sub(r'^[,.;:!?]+\s*', '', text)
        return text.strip()

    def _get_tool(self, lang):
        if language_tool_python is None:
            raise RuntimeError("language-tool-python is not installed in the active environment.")

        tool_lang = 'fi' if lang == 'fi' else 'en-US'
        if tool_lang not in self._tools:
            self._tools[tool_lang] = language_tool_python.LanguageTool(tool_lang)
        return self._tools[tool_lang]

    def finalize_text(self, text, lang='fi'):
        """Apply cleanup and grammar correction when available."""
        cleaned = self.pre_clean(text)

        try:
            tool = self._get_tool(lang)
        except Exception:
            return cleaned

        return tool.correct(cleaned)


sanitizer = TextSanitizer()


def prepare_text_for_db(raw_data, lang='fi'):
    """Return sanitized text ready for storage in ChromaDB."""
    return sanitizer.finalize_text(raw_data, lang=lang)


if __name__ == '__main__':
    raw_data = "Tota, se tiiviste malli XYZ pitää asentaa silleen kuivana [noise]."
    ready_for_db = prepare_text_for_db(raw_data, lang='fi')

    print(f"RAW: {raw_data}")
    print(f"DB READY: {ready_for_db}")
