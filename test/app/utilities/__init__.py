from flask import Blueprint

bp = Blueprint("utilities", __name__, template_folder="test-templates")

from app.utilities import routes  # noqa: E402,F401
