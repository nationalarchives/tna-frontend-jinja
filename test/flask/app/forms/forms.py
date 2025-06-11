from flask_wtf import FlaskForm
from tna_frontend_jinja.wtforms import (
    TnaCheckboxesInput,
    TnaCheckboxInput,
    TnaDateField,
    TnaDecimalInput,
    TnaMonthField,
    TnaPasswordInput,
    TnaProgressiveDateField,
    TnaRadioInput,
    TnaSelect,
    TnaSubmitInput,
    TnaTextArea,
    TnaTextInput,
    TnaYearField,
)
from tna_frontend_jinja.wtforms.validators import FutureDate, PastDate
from wtforms import (
    BooleanField,
    DecimalField,
    EmailField,
    PasswordField,
    RadioField,
    SelectField,
    SelectMultipleField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import Email, InputRequired, Length, NumberRange


class TextInputForm(FlaskForm):
    username = StringField(
        "Username",
        widget=TnaTextInput(),
        validators=[
            InputRequired(message="Enter a username"),
            Length(max=256, message="Usernames must be 256 characters or fewer"),
        ],
    )

    submit = SubmitField("Continue", widget=TnaSubmitInput())


class DateInputForm(FlaskForm):
    dob = TnaDateField(
        "Date of birth",
        validators=[
            InputRequired(message="Enter your date of birth"),
            PastDate(message="Date of birth must be in the past"),
        ],
    )

    submit = SubmitField("Continue", widget=TnaSubmitInput())


class DateInputMonthForm(FlaskForm):
    month_of_birth = TnaMonthField(
        "Month of birth",
        # invalid_date_error_message="Enter a valid month and year",
        validators=[
            InputRequired(message="Enter your month and year of birth"),
            PastDate(message="Date must be in the past"),
        ],
    )

    submit = SubmitField("Continue", widget=TnaSubmitInput())


class DateInputYearForm(FlaskForm):
    year_of_retirement = TnaYearField(
        "Planned year of retirement",
        invalid_date_error_message="Planned year of retirement must be a valid year",
        validators=[
            InputRequired(message="Enter a year for retirement"),
            FutureDate(message="Year of retirement must be in the future"),
        ],
    )

    submit = SubmitField("Continue", widget=TnaSubmitInput())


class DateInputProgressiveForm(FlaskForm):
    date_search = TnaProgressiveDateField(
        "Search for date",
        validators=[
            InputRequired(message="Enter a date"),
        ],
    )

    submit = SubmitField("Continue", widget=TnaSubmitInput())


class KitchenSinkForm(FlaskForm):
    username = StringField(
        "Username",
        widget=TnaTextInput(),
        validators=[
            InputRequired(message="Enter a username"),
            Length(max=256, message="Usernames must be 256 characters or fewer"),
        ],
    )

    password = PasswordField(
        "Password",
        validators=[
            InputRequired(message="Enter a password"),
        ],
        widget=TnaPasswordInput(),
    )

    email = EmailField(
        "Email address",
        validators=[
            InputRequired(message="Enter an email address"),
            Length(max=256, message="Email address must be 256 characters or fewer"),
            Email(message="Enter a valid email address"),
        ],
        description="We’ll only use this to send you a receipt",
        widget=TnaTextInput(),
    )

    height = DecimalField(
        "Height in centimetres",
        validators=[
            InputRequired(message="Enter a height"),
            NumberRange(
                min=1, max=272, message="Height must be between 1 cm and 272 cm"
            ),
        ],
        widget=TnaDecimalInput(),
    )

    remember = BooleanField(
        "I agree to terms and conditions",
        validators=[
            InputRequired(message="You must agree to the terms and conditions"),
        ],
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

    day_of_week = RadioField(
        "Day",
        choices=[("mon", "Monday"), ("tue", "Tuesday"), ("wed", "Wednesday")],
        validators=[
            InputRequired(message="Select a day"),
        ],
        widget=TnaRadioInput(),
    )

    birthday = TnaDateField(
        "Birthday",
        validators=[
            InputRequired(message="Enter a date"),
        ],
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
