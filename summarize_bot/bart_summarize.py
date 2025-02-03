from transformers import pipeline
from summarize_bot.predictor import Predictor
from summarize_bot.config import Config


class BartSummarize(Predictor):
    def __init__(self):
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn", truncation=True)

    def predict(self, text: str) -> str:
        if not text:
            raise ValueError("No text to summarize.")

        if len(text) < Config.max_length:
            return text

        summary = self.summarizer(
            text,
            max_length=Config.max_length,
            num_beams=Config.num_beams,
            min_length=Config.min_length,
            early_stopping=True,
        )

        if isinstance(summary, list) and summary:
            return summary[0]["summary_text"]
        raise ValueError("Summarization failed or returned an unexpected result.")
