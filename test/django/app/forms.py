from django import forms

# from tna_frontend_jinja.djangoforms.widgets import TnaTextInput


class NameForm(forms.Form):
    your_name = forms.CharField(label="Your name", max_length=100)

    # username = forms.CharField(
    #     "Username",
    #     widget=TnaTextInput(),
    #     # validators=[
    #     #     InputRequired(message="Enter an email address"),
    #     #     Length(max=256, message="Email address must be 256 characters or fewer"),
    #     # ],
    #     # description="We’ll only use this to send you a receipt",
    # )
