class LanguageMapper:
    def __init__(self):
        self.language_map = {
            "en": "English",
            "pt": "Portuguese",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "it": "Italian",
            "zh": "Chinese",
            "ja": "Japanese",
            "ko": "Korean",
            "ru": "Russian",
            "ar": "Arabic",
            "hi": "Hindi",
            "bn": "Bengali",
            "pa": "Punjabi",
            "jv": "Javanese",
            "ms": "Malay",
            "ur": "Urdu",
            "vi": "Vietnamese",
            "tl": "Tagalog",
            "fa": "Persian",
            "sw": "Swahili",
            "th": "Thai",
            "tr": "Turkish"
        }

    def get_language_name(self, abbreviation: str) -> str:
        return self.language_map.get(abbreviation, "English")
