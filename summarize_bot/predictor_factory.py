from summarize_bot.config import Config
from summarize_bot.predictor import Predictor


class PredictorFactory:
    """
    Factory class that dynamically instantiates and returns the correct Predictor
    based on the configuration. This approach ensures that only the configured model
    is loaded at startup.
    """

    def __new__(cls, *args, **kwargs) -> Predictor:
        if Config.MODEL == "bart":
            from summarize_bot.bart_summarize import BartSummarize

            return BartSummarize(*args, **kwargs)
        elif Config.MODEL == "pegasus":
            from summarize_bot.pegasus_summarize import PegasusSummarize

            return PegasusSummarize(*args, **kwargs)
        elif Config.MODEL == "t5":
            from summarize_bot.t5_summarize import T5Summarize

            return T5Summarize(*args, **kwargs)
        else:
            raise ValueError(f"Unsupported NER model: {Config.MODEL}")
