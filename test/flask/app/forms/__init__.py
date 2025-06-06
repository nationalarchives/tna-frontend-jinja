from flask import Blueprint

bp = Blueprint("forms", __name__, template_folder="test-templates")

from app.forms import routes  # noqa: E402,F401
