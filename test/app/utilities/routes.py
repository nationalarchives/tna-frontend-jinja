import json

from app.utilities import bp
from flask import render_template, request


def render_component(template):
    params = request.args.get("params")
    context = json.loads(params) if params else {}
    return render_template(template, context=context)


@bp.route("/grid")
def grid():
    return render_component("grid.html")
