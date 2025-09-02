from quart import Quart
from summarize_bot import router


def create_app():
    app = Quart(__name__)
    app.config.from_object("summarize_bot.config.Config")

    init(app)

    return app


def init(app: Quart):
    router.init(app)


if __name__ == "__main__":
    create_app().run()
