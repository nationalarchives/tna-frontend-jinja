from flask import Flask


def create_app():
    app = Flask(__name__)

    from .components import bp as components_bp

    app.register_blueprint(components_bp)

    return app
