from flask import Flask


def create_app():
    app = Flask(__name__, template_folder="../../tna_frontend_jinja/templates")

    from .components import bp as components_bp
    from .templates import bp as templates_bp

    app.register_blueprint(components_bp, url_prefix="/components")
    app.register_blueprint(templates_bp, url_prefix="/templates")

    return app
