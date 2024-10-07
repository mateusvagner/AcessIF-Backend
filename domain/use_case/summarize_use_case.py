from database.model.audio_transcription import AudioTranscription
from database.model.summary import Summary
from llm_summarizer.language_util import LanguageMapper
from llm_summarizer.summarizer_interface import SummarizerInterface
from service.db_service import DbService


class SummarizeUseCase:

    def __init__(self, llm_summarizer: SummarizerInterface, db_service: DbService):
        self.llm_summarizer = llm_summarizer
        self.db_service = db_service

    def execute(self, audio_transcription: AudioTranscription) -> Summary:
        saved_summary = Summary.query.filter_by(transcription_id=audio_transcription.id).first()

        if saved_summary:
            return saved_summary

        language_mapper = LanguageMapper()
        audio_transcription_language = language_mapper.get_language_name(audio_transcription.language)

        summary_text = self.llm_summarizer.summarize(text=audio_transcription.text,
                                                     language=audio_transcription_language)

        summary = Summary(text=summary_text, transcription_id=audio_transcription.id)

        self.db_service.save_summary(summary)

        return summary
