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
from wtforms.validators import InputRequired, Length


class ExampleForm(FlaskForm):
    username = StringField(
        "Username",
        widget=TnaTextInput(),
        validators=[
            InputRequired(message="Enter an email address"),
            Length(
                max=256, message="Email address must be 256 characters or fewer"
            ),
        ],
        description="We’ll only use this to send you a receipt",
    )
    password = StringField(
        "Password",
        validators=[
            InputRequired(message="Enter a password"),
        ],
        widget=TnaPasswordInput(),
    )
    remember = BooleanField(
        "Remember me",
        widget=TnaCheckboxInput(),
    )
    shopping = SelectMultipleField(
        "Shopping list",
        validators=[
            InputRequired(message="Select an item"),
        ],
        choices=[("cpp", "C++"), ("py", "Python"), ("text", "Plain Text")],
        widget=TnaCheckboxesInput(),
    )
    day = RadioField(
        "Day",
        choices=[("mon", "Monday"), ("tue", "Tuesday"), ("wed", "Wednesday")],
        validators=[
            InputRequired(message="Select a day"),
        ],
        widget=TnaRadioInput(),
    )
    birthday = DateField(
        "Birthday",
        validators=[
            InputRequired(message="Enter a date"),
        ],
        widget=TnaDateInput(),
    )
    message = TextAreaField(
        "Message",
        validators=[
            InputRequired(message="Enter a message"),
        ],
        widget=TnaTextArea(),
    )
    order = SelectField(
        "Order",
        choices=[
            ("", "None"),
            ("date", "Date"),
            ("relevance", "Relevance"),
            ("popularity", "Popularity"),
        ],
        validators=[
            InputRequired(message="Select an order"),
        ],
        widget=TnaSelect(),
    )

    submit = SubmitField("Continue", widget=TnaSubmitInput())


@bp.route("/", methods=["GET", "POST"])
def index():
    form = ExampleForm()
    if form.validate_on_submit():
        return redirect(url_for("forms.index", status="Success"))
    return render_template("example-form.html", form=form)
