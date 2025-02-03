from transformers import pipeline
from summarize_bot.predictor import Predictor
from summarize_bot.config import Config


class BartSummarize(Predictor):
    def __init__(self):
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        self.max_length = Config.max_length
        self.min_length = Config.min_length

    def predict(self, text: str) -> str:
        if not text:
            raise ValueError("No text to summarize.")

        if len(text) < self.max_length:
            return text

        summary = self.summarizer(text, max_length=self.max_length, min_length=self.min_length)

        if isinstance(summary, list) and summary:
            return summary[0]["summary_text"]
        raise ValueError("Summarization failed or returned an unexpected result.")
