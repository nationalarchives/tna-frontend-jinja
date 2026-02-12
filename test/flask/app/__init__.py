from app.components import bp as components_bp
from app.forms import bp as forms_bp
from app.templates import bp as templates_bp
from app.utilities import bp as utilities_bp
from flask import Flask

# from flask_wtf.csrf import CSRFError, CSRFProtect
from jinja2 import ChoiceLoader, PackageLoader
from tna_frontend_jinja.wtforms.helpers import WTFormsHelpers

app = Flask(
    __name__, static_url_path="/static", static_folder="/app/node_modules"
)

# csrf = CSRFProtect(app)

# @app.errorhandler(CSRFError)
# def handle_csrf_error(e):
#     return render_template("csrf_error.html", reason=e.description), 400

app.config["SECRET_KEY"] = "abc123"

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
