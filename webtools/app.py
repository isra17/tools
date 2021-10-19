from flask import Flask

def create_app():
    app = Flask(__name__)
    env_config = os.getenv("APP_SETTINGS", "webtools.config.DevelopmentConfig")
    app.config.from_object(env_config)

    @app.route("/")
    def index():
        return "Hello World!"
