from flask import Blueprint

bp = Blueprint("utilities", __name__)

from test.utilities import routes  # noqa: E402,F401
