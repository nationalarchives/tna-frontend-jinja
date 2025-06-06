from django.forms import CharField
from tna_frontend_jinja.djangoforms.forms import TnaForm
from tna_frontend_jinja.djangoforms.widgets import TnaTextInput


class NameForm(TnaForm):

    username = CharField(
        label="Username",
        max_length=256,
        widget=TnaTextInput(),
        required=True,
        # validators=[
        #     InputRequired(message="Enter an email address"),
        #     Length(max=256, message="Email address must be 256 characters or fewer"),
        # ],
        # description="We’ll only use this to send you a receipt",
    )
