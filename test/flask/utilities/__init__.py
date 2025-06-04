from flask import Blueprint

bp = Blueprint("utilities", __name__)

from test.flask.utilities import routes  # noqa: E402,F401
