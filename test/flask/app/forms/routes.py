from app.forms import bp
from app.forms.forms import (
    CheckboxesForm,
    CheckboxForm,
    DateInputForm,
    DateInputMonthForm,
    DateInputProgressiveForm,
    DateInputYearForm,
    KitchenSinkForm,
    RadiosForm,
    SelectForm,
    TextareaForm,
    TextInputDecimalForm,
    TextInputEmailForm,
    TextInputFloatForm,
    TextInputForm,
    TextInputIntegerForm,
    TextInputPasswordForm,
    TextInputURLForm,
)
from flask import current_app, render_template, url_for


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
    success = form.validate_on_submit()
    return render_template("single-field.html", form=form, success=success)


@bp.route("/text-input-email/", methods=["GET", "POST"])
def text_input_email():
    form = TextInputEmailForm()
    success = form.validate_on_submit()
    return render_template("single-field.html", form=form, success=success)


@bp.route("/text-input-password/", methods=["GET", "POST"])
def text_input_password():
    form = TextInputPasswordForm()
    success = form.validate_on_submit()
    return render_template("single-field.html", form=form, success=success)


@bp.route("/text-input-integer/", methods=["GET", "POST"])
def text_input_integer():
    form = TextInputIntegerForm()
    success = form.validate_on_submit()
    return render_template("single-field.html", form=form, success=success)


@bp.route("/text-input-decimal/", methods=["GET", "POST"])
def text_input_decimal():
    form = TextInputDecimalForm()
    success = form.validate_on_submit()
    return render_template("single-field.html", form=form, success=success)


@bp.route("/text-input-float/", methods=["GET", "POST"])
def text_input_float():
    form = TextInputFloatForm()
    success = form.validate_on_submit()
    return render_template("single-field.html", form=form, success=success)


@bp.route("/text-input-url/", methods=["GET", "POST"])
def text_input_url():
    form = TextInputURLForm()
    success = form.validate_on_submit()
    return render_template("single-field.html", form=form, success=success)


@bp.route("/date-input/", methods=["GET", "POST"])
def date_input():
    form = DateInputForm()
    success = form.validate_on_submit()
    return render_template("single-field.html", form=form, success=success)


@bp.route("/date-input-month/", methods=["GET", "POST"])
def date_input_month():
    form = DateInputMonthForm()
    success = form.validate_on_submit()
    return render_template("single-field.html", form=form, success=success)


@bp.route("/date-input-year/", methods=["GET", "POST"])
def date_input_year():
    form = DateInputYearForm()
    success = form.validate_on_submit()
    return render_template("single-field.html", form=form, success=success)


@bp.route("/date-input-progressive/", methods=["GET", "POST"])
def date_input_progressive():
    form = DateInputProgressiveForm()
    success = form.validate_on_submit()
    return render_template("single-field.html", form=form, success=success)


@bp.route("/checkbox/", methods=["GET", "POST"])
def checkbox():
    form = CheckboxForm()
    success = form.validate_on_submit()
    return render_template("checkbox.html", form=form, success=success)


@bp.route("/checkboxes/", methods=["GET", "POST"])
def checkboxes():
    form = CheckboxesForm()
    success = form.validate_on_submit()
    return render_template("single-field.html", form=form, success=success)


@bp.route("/radios/", methods=["GET", "POST"])
def radios():
    form = RadiosForm()
    success = form.validate_on_submit()
    return render_template("single-field.html", form=form, success=success)


@bp.route("/select/", methods=["GET", "POST"])
def select():
    form = SelectForm()
    success = form.validate_on_submit()
    return render_template("single-field.html", form=form, success=success)


@bp.route("/textarea/", methods=["GET", "POST"])
def textarea():
    form = TextareaForm()
    success = form.validate_on_submit()
    return render_template("single-field.html", form=form, success=success)


@bp.route("/kitchen-sink/", methods=["GET", "POST"])
def kitchen_sink():
    form = KitchenSinkForm()
    success = form.validate_on_submit()
    return render_template("kitchen-sink.html", form=form, success=success)
