from flask import Blueprint

bp = Blueprint("components", __name__, template_folder="test-templates")

from app.components import routes  # noqa: E402,F401
