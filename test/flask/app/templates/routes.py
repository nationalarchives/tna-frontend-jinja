import json

from app.templates import bp
from flask import render_template, request


@bp.route("/<path:template>")
def base(template):
    params = request.args.get("params")
    return render_template(template, **json.loads(params) if params else {})
