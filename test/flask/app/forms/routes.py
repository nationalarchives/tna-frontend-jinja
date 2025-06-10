from app.forms import bp
from app.forms.forms import (
    DateInputForm,
    DateInputMonthForm,
    DateInputProgressiveForm,
    DateInputYearForm,
    KitchenSinkForm,
    TextInputForm,
)
from flask import current_app, redirect, render_template, url_for


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@bp.route("/")
def index():
    urls = {}
    for rule in current_app.url_map.iter_rules():
        if (
            "GET" in rule.methods
            and has_no_empty_params(rule)
            and rule.endpoint not in ["forms.index", "forms.success"]
            and rule.endpoint.startswith("forms.")
        ):
            urls[rule.endpoint] = url_for(rule.endpoint, **(rule.defaults or {}))
    return render_template("index.html", urls=urls)


@bp.route("/text-input/", methods=["GET", "POST"])
def text_input():
    form = TextInputForm()
    if form.validate_on_submit():
        return redirect(url_for("forms.success"))
    return render_template("text-input.html", form=form)


@bp.route("/date-input/", methods=["GET", "POST"])
def date_input():
    form = DateInputForm()
    if form.validate_on_submit():
        return redirect(url_for("forms.success"))
    return render_template("date-input.html", form=form)


@bp.route("/date-input-month/", methods=["GET", "POST"])
def date_input_month():
    form = DateInputMonthForm()
    if form.validate_on_submit():
        return redirect(url_for("forms.success"))
    return render_template("date-input-month.html", form=form)


@bp.route("/date-input-year/", methods=["GET", "POST"])
def date_input_year():
    form = DateInputYearForm()
    if form.validate_on_submit():
        return redirect(url_for("forms.success"))
    return render_template("date-input-year.html", form=form)


@bp.route("/date-input-progressive/", methods=["GET", "POST"])
def date_input_progressive():
    form = DateInputProgressiveForm()
    if form.validate_on_submit():
        print("Form data:", form.data)
        # return redirect(url_for("forms.success"))
    return render_template("date-input-progressive.html", form=form)


@bp.route("/kitchen-sink/", methods=["GET", "POST"])
def kitchen_sink():
    form = KitchenSinkForm()
    if form.validate_on_submit():
        return redirect(url_for("forms.success"))
    return render_template("kitchen-sink.html", form=form)


@bp.route("/success/")
def success():
    return render_template("success.html")
