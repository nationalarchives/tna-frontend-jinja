from flask import Blueprint

bp = Blueprint("layouts", __name__)

from test.app.layouts import routes  # noqa: E402,F401
