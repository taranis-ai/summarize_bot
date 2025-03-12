from flask import Flask, Blueprint, jsonify, request
from flask.views import MethodView

from summarize_bot.predictor_factory import PredictorFactory
from summarize_bot.predictor import Predictor
from summarize_bot.decorators import api_key_required
from summarize_bot.decorators import debug_request


class SummarizeText(MethodView):
    def __init__(self, processor: Predictor) -> None:
        super().__init__()
        self.processor = processor

    @debug_request
    @api_key_required
    def post(self):
        data = request.get_json()
        text = data.get("text", "")
        summary = self.processor.predict(text)
        return jsonify({"summary": summary})


class HealthCheck(MethodView):
    @debug_request
    def get(self):
        return jsonify({"status": "ok"})


class ModelInfo(MethodView):
    def __init__(self, processor: Predictor):
        super().__init__()
        self.processor = processor
    @debug_request
    def get(self):
        return jsonify(self.processor.modelinfo)


def init(app: Flask):
    summarizer = PredictorFactory()
    app.url_map.strict_slashes = False

    summarize_bp = Blueprint("predict", __name__)
    summarize_bp.add_url_rule("/", view_func=SummarizeText.as_view("summarize", processor=summarizer))
    summarize_bp.add_url_rule("/health", view_func=HealthCheck.as_view("health"))
    summarize_bp.add_url_rule("/modelinfo", view_func=ModelInfo.as_view("modelinfo", processor=summarizer))
    app.register_blueprint(summarize_bp)
