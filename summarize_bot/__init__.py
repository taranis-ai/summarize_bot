from flask import Flask
from summarize_bot import router
from summarize_bot.summarize import Summarize


def create_app():
    app = Flask(__name__)
    app.config.from_object("summarize_bot.config.Config")

    with app.app_context():
        init(app)

    return app


def init(app: Flask):
    summarizer = Summarize()
    router.init(app, summarizer)


if __name__ == "__main__":
    create_app().run()
