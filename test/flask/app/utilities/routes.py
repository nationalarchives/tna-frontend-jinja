import json

from flask import render_template, request

from app.utilities import bp


def render_component(template):
    params_str = request.args.get("params")
    params = json.loads(params_str) if params_str else {}
    return render_template(template, params=params)


@bp.route("/grid")
def grid():
    return render_component("utilities/grid.html")
