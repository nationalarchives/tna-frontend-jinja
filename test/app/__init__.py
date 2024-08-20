import os
import sys

from flask import Flask

from .components import bp as components_bp
from .forms import bp as forms_bp
# from .forms.routes import WTFormsHelpers
from .templates import bp as templates_bp
from .utilities import bp as utilities_bp


sys.path.append('/home/app/')

from tna_frontend_jinja.wtforms.widgets import WTFormsHelpers

app = Flask(__name__, template_folder="/home/app/tna_frontend_jinja/templates")

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")


@app.route("/healthcheck/live/")
def healthcheck():
    return "ok"


app.register_blueprint(components_bp, url_prefix="/components")
app.register_blueprint(utilities_bp, url_prefix="/utilities")
app.register_blueprint(templates_bp, url_prefix="/templates")
app.register_blueprint(forms_bp, url_prefix="/forms")

WTFormsHelpers(app)
