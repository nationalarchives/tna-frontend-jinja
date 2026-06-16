import json

from flask import render_template, request

from app.templates import bp


@bp.route("/<path:template>")
def base(template):
    params = request.args.get("params")
    return render_template(template, **json.loads(params) if params else {})
