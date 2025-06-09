from app.forms import bp
from app.forms.forms import DateInputsForm, KitchenSinkForm, TextInputForm
from flask import redirect, render_template, url_for


@bp.route("/text-input/", methods=["GET", "POST"])
def text_input():
    form = TextInputForm()
    if form.validate_on_submit():
        return redirect(url_for("forms.success"))
    return render_template("text-input.html", form=form)


@bp.route("/date-input/", methods=["GET", "POST"])
def date_input():
    form = DateInputsForm()
    if form.validate_on_submit():
        return redirect(url_for("forms.success"))
    return render_template("date-input.html", form=form)


@bp.route("/kitchen-sink/", methods=["GET", "POST"])
def kitchen_sink():
    form = KitchenSinkForm()
    if form.validate_on_submit():
        return redirect(url_for("forms.success"))
    return render_template("kitchen-sink.html", form=form)


@bp.route("/success/")
def success():
    return render_template("success.html")
