import sys
from app.forms import bp
from flask import redirect, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Email, InputRequired, Length

sys.path.append('/home/app/')
from tna_frontend_jinja.wtforms.widgets import GovTextInput, GovSubmitInput


class ExampleForm(FlaskForm):
    email_address = StringField(
        "Email address",
        widget=GovTextInput(),
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

    submit = SubmitField("Continue", widget=GovSubmitInput())


@bp.route("/", methods=["GET", "POST"])
def index():
    form = ExampleForm()
    if form.validate_on_submit():
        return redirect(url_for("forms.index"))
    return render_template("example-form.html", form=form)
