import json

from app.templates import bp
from flask import render_template, request


@bp.route("/base")
def base():
    params = request.args.get("params")
    context = json.loads(params) if params else {}
    return render_template("layouts/base.html", context=context)
