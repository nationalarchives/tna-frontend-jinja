from test.forms import bp

from flask import redirect, render_template, url_for
from flask_wtf import FlaskForm
from tna_frontend_jinja.wtforms.widgets import (
    TnaCheckboxesInput,
    TnaCheckboxInput,
    TnaDateInput,
    TnaPasswordInput,
    TnaRadioInput,
    TnaSelect,
    TnaSubmitInput,
    TnaTextArea,
    TnaTextInput,
)
from wtforms import (
    BooleanField,
    DateField,
    RadioField,
    SelectField,
    SelectMultipleField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import Email, InputRequired, Length


class ExampleForm(FlaskForm):
    email_address = StringField(
        "Email address",
        widget=TnaTextInput(),
        validators=[
            InputRequired(message="Enter an email address"),
            Length(
                max=256, message="Email address must be 256 characters or fewer"
            ),
            Email(
                message="Enter an email address in the correct format, like name@example.com"
            ),
        ],
        description="We’ll only use this to send you a receipt",
    )
    password = StringField(
        "Password",
        widget=TnaPasswordInput(),
    )
    remember = BooleanField(
        "Remember me",
        widget=TnaCheckboxInput(),
    )
    shopping = SelectMultipleField(
        "Shopping list",
        choices=[("cpp", "C++"), ("py", "Python"), ("text", "Plain Text")],
        widget=TnaCheckboxesInput(),
    )
    day = RadioField(
        "Day",
        choices=[("mon", "Monday"), ("tue", "Tuesday"), ("wed", "Wednesday")],
        widget=TnaRadioInput(),
    )
    birthday = DateField(
        "Birthday",
        widget=TnaDateInput(),
    )
    message = TextAreaField(
        "Message",
        widget=TnaTextArea(),
    )
    order = SelectField(
        "Order",
        choices=[
            ("date", "Date"),
            ("relevance", "Relevance"),
            ("popularity", "Popularity"),
        ],
        widget=TnaSelect(),
    )

    submit = SubmitField("Continue", widget=TnaSubmitInput())


@bp.route("/", methods=["GET", "POST"])
def index():
    form = ExampleForm()
    if form.validate_on_submit():
        return redirect(url_for("forms.index"))
    return render_template("example-form.html", form=form)
