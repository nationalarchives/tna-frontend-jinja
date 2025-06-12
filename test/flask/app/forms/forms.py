from flask_wtf import FlaskForm
from tna_frontend_jinja.wtforms import (
    TnaCheckboxesInput,
    TnaCheckboxInput,
    TnaDateField,
    TnaDecimalInput,
    TnaEmailInput,
    TnaMonthField,
    TnaPasswordInput,
    TnaProgressiveDateField,
    TnaRadioInput,
    TnaSearchInput,
    TnaSelect,
    TnaSubmitInput,
    TnaTextArea,
    TnaTextInput,
    TnaUrlInput,
    TnaYearField,
)
from tna_frontend_jinja.wtforms import validators as tna_frontend_validators
from wtforms import (
    BooleanField,
    DecimalField,
    EmailField,
    PasswordField,
    RadioField,
    SearchField,
    SelectField,
    SelectMultipleField,
    StringField,
    SubmitField,
    TextAreaField,
    URLField,
    validators,
)


class TextInputForm(FlaskForm):
    username = StringField(
        "Username",
        widget=TnaTextInput(),
        validators=[
            validators.InputRequired(message="Enter a username"),
            validators.Length(
                max=256, message="Usernames must be 256 characters or fewer"
            ),
        ],
    )

    submit = SubmitField("Continue", widget=TnaSubmitInput())


class DateInputForm(FlaskForm):
    dob = TnaDateField(
        "Date of birth",
        validators=[
            validators.InputRequired(message="Enter your date of birth"),
            tna_frontend_validators.PastDate(
                message="Date of birth must be in the past"
            ),
        ],
    )

    submit = SubmitField("Continue", widget=TnaSubmitInput())


class DateInputMonthForm(FlaskForm):
    month_of_birth = TnaMonthField(
        "Month of birth",
        # invalid_date_error_message="Enter a valid month and year",
        validators=[
            validators.InputRequired(message="Enter your month and year of birth"),
            tna_frontend_validators.PastDate(message="Date must be in the past"),
        ],
    )

    submit = SubmitField("Continue", widget=TnaSubmitInput())


class DateInputYearForm(FlaskForm):
    year_of_retirement = TnaYearField(
        "Planned year of retirement",
        invalid_date_error_message="Planned year of retirement must be a valid year",
        validators=[
            validators.InputRequired(message="Enter a year for retirement"),
            tna_frontend_validators.FutureDate(
                message="Year of retirement must be in the future"
            ),
        ],
    )

    submit = SubmitField("Continue", widget=TnaSubmitInput())


class DateInputProgressiveForm(FlaskForm):
    date_search = TnaProgressiveDateField(
        "Search for date",
        validators=[
            validators.InputRequired(message="Enter a date"),
        ],
    )

    submit = SubmitField("Continue", widget=TnaSubmitInput())


class KitchenSinkForm(FlaskForm):
    search = SearchField(
        "Search",
        widget=TnaSearchInput(),
    )

    username = StringField(
        "Username",
        widget=TnaTextInput(),
        validators=[
            validators.InputRequired(message="Enter a username"),
            validators.Length(
                max=256, message="Usernames must be 256 characters or fewer"
            ),
        ],
    )

    password = PasswordField(
        "Password",
        validators=[
            validators.InputRequired(message="Enter a password"),
        ],
        widget=TnaPasswordInput(),
    )

    email = EmailField(
        "Email address",
        validators=[
            validators.InputRequired(message="Enter an email address"),
            validators.Length(
                max=256, message="Email address must be 256 characters or fewer"
            ),
            validators.Email(message="Enter a valid email address"),
        ],
        description="We’ll only use this to send you a receipt",
        widget=TnaEmailInput(),
    )

    height = DecimalField(
        "Height in centimetres",
        validators=[
            validators.InputRequired(message="Enter a height"),
            validators.NumberRange(
                min=1, max=272, message="Height must be between 1 cm and 272 cm"
            ),
        ],
        widget=TnaDecimalInput(),
    )

    url = URLField(
        "Site URL",
        validators=[
            validators.InputRequired(message="Enter a URL"),
            validators.URL(
                message="Enter a valid URL",
            ),
        ],
        widget=TnaUrlInput(),
    )

    remember = BooleanField(
        "I agree to terms and conditions",
        validators=[
            validators.InputRequired(
                message="You must agree to the terms and conditions"
            ),
        ],
        widget=TnaCheckboxInput(),
    )

    shopping = SelectMultipleField(
        "Shopping list",
        validators=[
            validators.InputRequired(message="Select an item"),
        ],
        choices=[("cpp", "C++"), ("py", "Python"), ("text", "Plain Text")],
        widget=TnaCheckboxesInput(),
    )

    day_of_week = RadioField(
        "Day",
        choices=[("mon", "Monday"), ("tue", "Tuesday"), ("wed", "Wednesday")],
        validators=[
            validators.InputRequired(message="Select a day"),
        ],
        widget=TnaRadioInput(),
    )

    birthday = TnaDateField(
        "Birthday",
        validators=[
            validators.InputRequired(message="Enter a date"),
        ],
    )

    message = TextAreaField(
        "Message",
        validators=[
            validators.InputRequired(message="Enter a message"),
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
            validators.InputRequired(message="Select an order"),
        ],
        widget=TnaSelect(),
    )

    submit = SubmitField("Continue", widget=TnaSubmitInput())
