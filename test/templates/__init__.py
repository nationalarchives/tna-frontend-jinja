from flask import Blueprint

bp = Blueprint("templates", __name__, template_folder="../templates")

from test.templates import routes  # noqa: E402,F401
