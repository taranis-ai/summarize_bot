from flask import Flask, Blueprint, jsonify, request
from flask.views import MethodView

from summarize_bot.summarize import Summarize


class SummarizeText(MethodView):
    def __init__(self, summarizer: Summarize) -> None:
        super().__init__()
        self.summarizer = summarizer

    def post(self):
        data = request.get_json()
        text = data.get("text", "")
        language = data.get("language", "en")
        summary = self.summarizer.predict(text, language)
        return jsonify({"summary": summary})


class HealthCheck(MethodView):
    def get(self):
        return jsonify({"status": "ok"})


def init(app: Flask, summarizer: Summarize):
    app.url_map.strict_slashes = False

    summarize_bp = Blueprint("predict", __name__)
    summarize_bp.add_url_rule("/", view_func=SummarizeText.as_view("summarize", summarizer=summarizer))
    summarize_bp.add_url_rule("/health", view_func=HealthCheck.as_view("health"))
    app.register_blueprint(summarize_bp)
