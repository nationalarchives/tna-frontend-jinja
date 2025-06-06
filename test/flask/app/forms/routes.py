from app.forms import bp
from app.forms.forms import KitchenSinkForm
from flask import redirect, render_template, url_for


@bp.route("/kitchen-sink", methods=["GET", "POST"])
def kitchen_sink():
    form = KitchenSinkForm()
    if form.validate_on_submit():
        return redirect(url_for("forms.index", status="Success"))
    return render_template("example-form.html", form=form)
