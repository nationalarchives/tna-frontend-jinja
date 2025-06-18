import decimal

from flask_wtf import FlaskForm
from tna_frontend_jinja.wtforms import (
    TnaCheckboxesWidget,
    TnaCheckboxWidget,
    TnaDateField,
    TnaEmailInputWidget,
    TnaMonthField,
    TnaNumberInputWidget,
    TnaPasswordWidget,
    TnaProgressiveDateField,
    TnaRadiosWidget,
    TnaSearchFieldWidget,
    TnaSelectWidget,
    TnaTelInputWidget,
    TnaTextareaWidget,
    TnaTextInputWidget,
    TnaUrlInputWidget,
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
        widget=TnaTextInputWidget(),
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
        widget=TnaEmailInputWidget(),
        validators=[
            validators.InputRequired(message="Enter an email address"),
            validators.Email(message="Enter a valid email address"),
        ],
    )


class TextInputPasswordForm(FlaskForm):
    field = PasswordField(
        "Password",
        widget=TnaPasswordWidget(),
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
        widget=TnaNumberInputWidget(),
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
        widget=TnaNumberInputWidget(),
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
        widget=TnaNumberInputWidget(),
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
        widget=TnaUrlInputWidget(),
    )


class TextInputTelForm(FlaskForm):
    field = TelField(
        "Phone number",
        validators=[
            validators.InputRequired(message="Enter a phone number"),
            validators.Regexp(
                regex="^[0-9 ()-+]{11,}$", message="Enter a valid phone number"
            ),
        ],
        widget=TnaTelInputWidget(),
    )


class DateInputForm(FlaskForm):
    field = TnaDateField(
        "Date of birth",
        description="Enter your date of birth in the format DD MM YYYY",
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
        description="Enter your month of birth in the format MM YYYY",
        validators=[
            validators.InputRequired(message="Enter your month and year of birth"),
            tna_frontend_validators.PastDate(message="Date must be in the past"),
        ],
    )


class DateInputYearForm(FlaskForm):
    field = TnaYearField(
        "Planned year of retirement",
        description="Enter your planned year of retirement in the format YY or YYYY",
        allow_two_digit_year=True,
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
        description="Enter a year, year and month or a full date",
        validators=[
            validators.Optional(),
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
        widget=TnaCheckboxWidget(),
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
        widget=TnaCheckboxesWidget(),
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
        widget=TnaRadiosWidget(),
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
        widget=TnaSelectWidget(),
    )


class TextareaForm(FlaskForm):
    field = TextAreaField(
        "Message",
        validators=[
            validators.InputRequired(message="Enter a message"),
        ],
        widget=TnaTextareaWidget(),
    )


class SearchForm(FlaskForm):
    field = SearchField(
        "Search",
        widget=TnaSearchFieldWidget(),
    )


class KitchenSinkForm(FlaskForm):
    search = SearchField(
        "Search",
        widget=TnaSearchFieldWidget(),
    )

    username = StringField(
        "Username",
        widget=TnaTextInputWidget(),
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
        widget=TnaPasswordWidget(),
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
        widget=TnaEmailInputWidget(),
    )

    height = DecimalField(
        "Height in centimetres",
        validators=[
            validators.InputRequired(message="Enter a height"),
            validators.NumberRange(
                min=1, max=272, message="Height must be between 1 cm and 272 cm"
            ),
        ],
        widget=TnaNumberInputWidget(),
    )

    url = URLField(
        "Site URL",
        validators=[
            validators.InputRequired(message="Enter a URL"),
            validators.URL(
                message="Enter a valid URL",
            ),
        ],
        widget=TnaUrlInputWidget(),
    )

    remember = BooleanField(
        "I agree to terms and conditions",
        validators=[
            validators.InputRequired(
                message="You must agree to the terms and conditions"
            ),
        ],
        widget=TnaCheckboxWidget(),
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
        widget=TnaCheckboxesWidget(),
    )

    day_of_week = RadioField(
        "Day",
        choices=[("mon", "Monday"), ("tue", "Tuesday"), ("wed", "Wednesday")],
        validators=[
            validators.InputRequired(message="Select a day"),
        ],
        widget=TnaRadiosWidget(),
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
        widget=TnaTextareaWidget(),
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
        widget=TnaSelectWidget(),
    )
