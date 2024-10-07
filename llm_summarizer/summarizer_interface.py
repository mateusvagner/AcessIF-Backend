from abc import ABC, abstractmethod


class SummarizerInterface(ABC):
    @abstractmethod
    def summarize(self, text: str, language: str) -> str:
        """Get summary a text and return its summary"""
        pass
