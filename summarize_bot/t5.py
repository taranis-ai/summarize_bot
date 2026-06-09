from transformers import pipeline, T5Tokenizer
from summarize_bot.config import Config
from typing import Any
from summarize_bot.utils import build_story_input_text


class T5:
    model_name = "deutsche-telekom/mt5-small-sum-de-en-v1"

    def __init__(self):
        tokenizer = T5Tokenizer.from_pretrained(self.model_name, legacy=True)
        self.summarizer = pipeline("summarization", model=self.model_name, tokenizer=tokenizer)

    async def predict(self, news_items: list[dict[str, Any]] | None = None, text: str | None = None) -> dict[str, str]:
        if news_items:
            text_to_summarize = build_story_input_text(news_items)
        elif text:
            text_to_summarize = text
        else:
            raise ValueError("No input to summarize")

        if len(text_to_summarize) < Config.MAX_LEN:
            return {"summary": text_to_summarize}

        summary = self.summarizer(
            text_to_summarize,
            max_new_tokens=Config.MAX_LEN,
            num_beams=Config.NUM_BEAMS,
            min_length=Config.MIN_LEN,
            early_stopping=True,
        )

        if isinstance(summary, list) and summary:
            return {"summary": summary[0]["summary_text"]}
        raise ValueError("Summarization failed or returned an unexpected result.")
