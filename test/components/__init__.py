from flask import Blueprint

bp = Blueprint("components", __name__)

from test.components import routes  # noqa: E402,F401
