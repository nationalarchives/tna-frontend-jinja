import json
from test.flask.utilities import bp

from flask import render_template, request


def render_component(template):
    params_str = request.args.get("params")
    params = json.loads(params_str) if params_str else {}
    return render_template(template, params=params)


@bp.route("/grid")
def grid():
    return render_component("utilities/grid.html")
