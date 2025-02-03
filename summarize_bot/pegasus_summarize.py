from transformers import PegasusTokenizer, PegasusForConditionalGeneration
from summarize_bot.predictor import Predictor
from summarize_bot.config import Config


class PegasusSummarize(Predictor):
    def __init__(self):
        self.tokenizer = PegasusTokenizer.from_pretrained("google/pegasus-xsum")
        self.summarizer = PegasusForConditionalGeneration.from_pretrained("google/pegasus-xsum")
        self.max_length = Config.max_length
        self.min_length = Config.min_length

    def predict(self, text: str) -> str:
        if not text:
            raise ValueError("No text to summarize.")

        if len(text) < self.max_length:
            return text

        inputs = self.tokenizer(text, truncation=True, padding="longest", return_tensors="pt")
        summary_ids = self.summarizer.generate(
            inputs.input_ids, max_length=60, min_length=20, length_penalty=2.0, num_beams=4, early_stopping=True
        )
        return self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
