from flask import Blueprint

bp = Blueprint("templates", __name__, template_folder="../templates")

from test.app.templates import routes  # noqa: E402,F401
