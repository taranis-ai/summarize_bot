from quart import Quart, Blueprint, jsonify, request
from quart.views import MethodView

from summarize_bot.predictor_factory import PredictorFactory
from summarize_bot.predictor import Predictor
from summarize_bot.decorators import api_key_required


class SummarizeText(MethodView):
    def __init__(self, processor: Predictor) -> None:
        super().__init__()
        self.processor = processor

    @api_key_required
    async def post(self):
        data = await request.get_json()
        text = data.get("text", "")
        summary = await self.processor.predict(text)
        return jsonify({"summary": summary})


class HealthCheck(MethodView):
    async def get(self):
        return jsonify({"status": "ok"})


class ModelInfo(MethodView):
    def __init__(self, processor: Predictor):
        super().__init__()
        self.processor = processor

    async def get(self):
        return jsonify(await self.processor.modelinfo)


def init(app: Quart):
    summarizer = PredictorFactory()
    app.url_map.strict_slashes = False

    summarize_bp = Blueprint("predict", __name__)
    summarize_bp.add_url_rule("/", view_func=SummarizeText.as_view("summarize", processor=summarizer))
    summarize_bp.add_url_rule("/health", view_func=HealthCheck.as_view("health"))
    summarize_bp.add_url_rule("/modelinfo", view_func=ModelInfo.as_view("modelinfo", processor=summarizer))
    app.register_blueprint(summarize_bp)
