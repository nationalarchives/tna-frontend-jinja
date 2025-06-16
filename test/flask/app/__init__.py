import os

from app.components import bp as components_bp
from app.forms import bp as forms_bp
from app.templates import bp as templates_bp
from app.utilities import bp as utilities_bp
from flask import Flask
from jinja2 import ChoiceLoader, PackageLoader
from tna_frontend_jinja.wtforms.helpers import WTFormsHelpers

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

app.jinja_loader = ChoiceLoader(
    [
        PackageLoader("app"),
        PackageLoader("tna_frontend_jinja"),
    ]
)


@app.route("/healthcheck/live/")
def healthcheck():
    return "ok"


app.register_blueprint(components_bp, url_prefix="/components")
app.register_blueprint(utilities_bp, url_prefix="/utilities")
app.register_blueprint(templates_bp, url_prefix="/templates")
app.register_blueprint(forms_bp, url_prefix="/forms")

WTFormsHelpers(app)
