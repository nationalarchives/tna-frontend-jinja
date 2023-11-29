from test.app.components import bp

from flask import render_template


@bp.route("/")
def base():
    return render_template("layouts/base.html")
