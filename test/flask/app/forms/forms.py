import decimal

from flask_wtf import FlaskForm
from tna_frontend_jinja.wtforms import (
    TnaCheckboxesInput,
    TnaCheckboxInput,
    TnaDateField,
    TnaEmailInput,
    TnaMonthField,
    TnaNumberInput,
    TnaPasswordInput,
    TnaProgressiveDateField,
    TnaRadioInput,
    TnaSearchInput,
    TnaSelect,
    TnaTelInput,
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
    FloatField,
    IntegerField,
    PasswordField,
    RadioField,
    SearchField,
    SelectField,
    SelectMultipleField,
    StringField,
    TelField,
    TextAreaField,
    URLField,
    validators,
)


class TextInputForm(FlaskForm):
    field = StringField(
        "Username",
        description="This will be used to log in",
        widget=TnaTextInput(),
        validators=[
            validators.InputRequired(message="Enter a username"),
            validators.Length(
                max=256, message="Usernames must be 256 characters or fewer"
            ),
        ],
    )


class TextInputEmailForm(FlaskForm):
    field = EmailField(
        "Email address",
        widget=TnaEmailInput(),
        validators=[
            validators.InputRequired(message="Enter an email address"),
            validators.Email(message="Enter a valid email address"),
        ],
    )


class TextInputPasswordForm(FlaskForm):
    field = PasswordField(
        "Password",
        widget=TnaPasswordInput(),
        validators=[
            validators.InputRequired(message="Enter a password"),
            validators.Length(
                min=8, message="Password must be at least 8 characters long"
            ),
        ],
    )


class TextInputIntegerForm(FlaskForm):
    field = IntegerField(
        "Integer",
        validators=[
            validators.InputRequired(message="Enter a whole number between 1 and 99"),
            validators.NumberRange(
                min=1, max=99, message="Number must be between 1 and 99"
            ),
        ],
        widget=TnaNumberInput(),
    )


class TextInputDecimalForm(FlaskForm):
    field = DecimalField(
        "Decimal",
        places=2,
        rounding=decimal.ROUND_UP,
        validators=[
            validators.InputRequired(message="Enter a decimal between 1 and 10"),
            validators.NumberRange(
                min=1, max=10, message="Number must be between 1 and 10"
            ),
        ],
        widget=TnaNumberInput(),
    )


class TextInputFloatForm(FlaskForm):
    field = FloatField(
        "Float",
        validators=[
            validators.InputRequired(message="Enter a float value between 1 and 10"),
            validators.NumberRange(
                min=1, max=10, message="Number must be between 1 and 10"
            ),
        ],
        widget=TnaNumberInput(),
    )


class TextInputURLForm(FlaskForm):
    field = URLField(
        "Site URL",
        validators=[
            validators.InputRequired(message="Enter a URL"),
            validators.URL(
                message="Enter a valid URL",
            ),
        ],
        widget=TnaUrlInput(),
    )


class TextInputTelForm(FlaskForm):
    field = TelField(
        "Phone number",
        validators=[
            validators.InputRequired(message="Enter a phone number"),
            validators.Regexp(
                regex="^[\d \(\)\-\+]+$", message="Enter a valid phone number"
            ),
        ],
        widget=TnaTelInput(),
    )


class DateInputForm(FlaskForm):
    field = TnaDateField(
        "Date of birth",
        validators=[
            validators.InputRequired(message="Enter your date of birth"),
            tna_frontend_validators.PastDate(
                message="Date of birth must be in the past"
            ),
        ],
    )


class DateInputMonthForm(FlaskForm):
    field = TnaMonthField(
        "Month of birth",
        # invalid_date_error_message="Enter a valid month and year",
        validators=[
            validators.InputRequired(message="Enter your month and year of birth"),
            tna_frontend_validators.PastDate(message="Date must be in the past"),
        ],
    )


class DateInputYearForm(FlaskForm):
    field = TnaYearField(
        "Planned year of retirement",
        invalid_date_error_message="Planned year of retirement must be a valid year",
        validators=[
            validators.InputRequired(message="Enter a year for retirement"),
            tna_frontend_validators.FutureDate(
                message="Year of retirement must be in the future"
            ),
        ],
    )


class DateInputProgressiveForm(FlaskForm):
    field = TnaProgressiveDateField(
        "Search for date",
        validators=[
            validators.InputRequired(message="Enter a date"),
        ],
    )


class CheckboxForm(FlaskForm):
    field = BooleanField(
        "I agree to terms and conditions",
        validators=[
            validators.InputRequired(
                message="You must agree to the terms and conditions"
            ),
        ],
        widget=TnaCheckboxInput(),
    )


class CheckboxesForm(FlaskForm):
    field = SelectMultipleField(
        "Languages",
        description="Select up to two programming languages",
        validators=[
            validators.InputRequired(message="Select at least one item"),
            tna_frontend_validators.MaxOptions(
                max=2, message="You must select no more than 2 items"
            ),
        ],
        choices=[("cpp", "C++"), ("py", "Python"), ("php", "PHP")],
        widget=TnaCheckboxesInput(),
    )


class RadiosForm(FlaskForm):
    field = RadioField(
        "Level",
        choices=[
            ("1", "Apprentice"),
            ("2", "Junior"),
            ("3", "Mid-level"),
            ("4", "Senior"),
            ("5", "Lead"),
            ("6", "Principal"),
        ],
        validators=[
            validators.InputRequired(message="Select a level"),
        ],
        widget=TnaRadioInput(),
    )


class SelectForm(FlaskForm):
    field = SelectField(
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


class TextareaForm(FlaskForm):
    field = TextAreaField(
        "Message",
        validators=[
            validators.InputRequired(message="Enter a message"),
        ],
        widget=TnaTextArea(),
    )


class SearchForm(FlaskForm):
    field = SearchField(
        "Search",
        widget=TnaSearchInput(),
    )


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
                max=16, message="Usernames must be 16 characters or fewer"
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
        widget=TnaNumberInput(),
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
        description="Select up to two items",
        validators=[
            validators.InputRequired(message="Select at least one item"),
            tna_frontend_validators.MaxOptions(
                max=2, message="You must select no more than 2 items"
            ),
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
