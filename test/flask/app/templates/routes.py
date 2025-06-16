import json

from app.templates import bp
from flask import render_template, request


@bp.route("/base")
def base():
    params_str = request.args.get("params")
    params = json.loads(params_str) if params_str else {}
    return render_template("layouts/base.html", context=params)
