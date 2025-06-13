from django.core.validators import EmailValidator, MaxValueValidator
from django.forms import CharField
from tna_frontend_jinja.djangoforms.forms import TnaForm
from tna_frontend_jinja.djangoforms.widgets import TnaTextInput


class NameForm(TnaForm):
    username = CharField(
        label="Username",
        widget=TnaTextInput(attrs={"headingLevel": 2, "spellcheck": False}),
        required=True,
        error_messages={"required": "Please let us know what to call you!"},
        validators=[
            MaxValueValidator(256, message="Usernames must be 256 characters or fewer")
        ],
    )

    password = CharField(
        label="Password",
        widget=TnaTextInput(attrs={"headingLevel": 2, "spellcheck": False}),
        required=True,
    )

    email = CharField(
        label="Email address",
        widget=TnaTextInput(attrs={"headingLevel": 2, "spellcheck": False}),
        required=True,
        error_messages={"required": "Enter an email address"},
        validators=[
            MaxValueValidator(256, message="Usernames must be 256 characters or fewer"),
            EmailValidator(message="Enter a valid email address"),
        ],
        help_text="We’ll only use this to send you a receipt",
    )
