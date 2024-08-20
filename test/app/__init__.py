from flask import Flask
from .components import bp as components_bp
from .utilities import bp as utilities_bp
from .templates import bp as templates_bp

app = Flask(__name__, template_folder="/home/app/tna_frontend_jinja/templates")


@app.route("/ready/")
def ready():
    return "ok"


app.register_blueprint(components_bp, url_prefix="/components")
app.register_blueprint(utilities_bp, url_prefix="/utilities")
app.register_blueprint(templates_bp, url_prefix="/templates")
