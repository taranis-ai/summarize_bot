from transformers import pipeline


class Summarize:
    def __init__(self):
        self.summarizer_en = pipeline("summarization", model="facebook/bart-large-cnn")
        self.summarizer_de = self.summarizer_en

    def predict(self, text: str, language: str = "en", max_length: int = 160, min_length: int = 60) -> str:
        if not text:
            raise ValueError("No text to summarize.")

        if len(text) < max_length:
            return text

        summarizer = self.summarizer_de if language == "de" else self.summarizer_en
        summary = summarizer(text, max_length=max_length, min_length=min_length)

        if isinstance(summary, list) and summary:
            return summary[0]["summary_text"]
        raise ValueError("Summarization failed or returned an unexpected result.")
