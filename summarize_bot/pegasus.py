from transformers import PegasusTokenizer, PegasusForConditionalGeneration
from summarize_bot.config import Config
from typing import Any
from summarize_bot.utils import build_story_input_text

class Pegasus:
    model_name = "google/pegasus-xsum"

    def __init__(self):
        self.tokenizer = PegasusTokenizer.from_pretrained(self.model_name)
        self.summarizer = PegasusForConditionalGeneration.from_pretrained(self.model_name)

    async def predict(self, news_items: list[dict[str, Any]] | None = None, text: str | None = None) -> dict[str, str]:
        if news_items:
            text_to_summarize = build_story_input_text(news_items)
        elif text:
            text_to_summarize = text
        else:
            raise ValueError("No input to summarize")

        if len(text_to_summarize) < Config.MAX_LEN:
            return {"summary": text_to_summarize}

        inputs = self.tokenizer(text_to_summarize, truncation=True, padding="longest", return_tensors="pt")
        summary_ids = self.summarizer.generate(
            inputs.input_ids,
            max_new_tokens=Config.MAX_LEN,
            min_length=Config.MIN_LEN,
            num_beams=Config.NUM_BEAMS,
            early_stopping=True,
        )
        return {"summary": self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)}
