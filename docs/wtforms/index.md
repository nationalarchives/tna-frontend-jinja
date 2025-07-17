# WTForms integration

## 1. Install WTForms

```sh
poetry add Flask-WTF
```

## 2. Add the TNA Frontend Jinja WTForms helpers

```py
from flask import Flask
from tna_frontend_jinja.wtforms.helpers import WTFormsHelpers


def create_app():
    app = Flask(__name__)

    # ...application setup...

    WTFormsHelpers(app)
```

## 3. Form setup

### 3.1. Create a form with fields

- [Defining a WTForms form](https://wtforms.readthedocs.io/en/3.1.x/forms/#defining-forms)
- [WTForms fields](https://wtforms.readthedocs.io/en/3.1.x/fields/)
- [Supported WTForms fields](./field-widgets.md)
- [Custom TNA fields](./tna-fields.md)

```py
from flask_wtf import FlaskForm
from wtforms import (
    EmailField,
    StringField,
    SubmitField,
)


class TextInputForm(FlaskForm):
    username = StringField(
        "Username",
        description="This will be used to log in",
    )

    email = EmailField(
        "Email address",
    )

    submit = SubmitField(
        "Continue",
    )
```

### 3.2. Add some validation

- [WTForms validators](https://wtforms.readthedocs.io/en/3.1.x/validators/)
- [Custom TNA validators](./tna-validators.md)

```diff
from flask_wtf import FlaskForm
from wtforms import (
    EmailField,
    StringField,
    SubmitField,
+     validators,
)


class TextInputForm(FlaskForm):
    username = StringField(
        "Username",
        description="This will be used to log in",
+         validators=[
+             validators.InputRequired(message="Enter a username"),
+             validators.Length(
+                 max=32, message="Usernames must be 32 characters or fewer"
+             ),
+         ],
    )

    email = EmailField(
        "Email address",
+         validators=[
+             validators.InputRequired(message="Enter an email address"),
+             validators.Email(message="Enter a valid email address"),
+         ],
    )

    submit = SubmitField(
        "Continue",
    )
```

### 3.3. Use the TNA widgets

- [TNA WTForms field widgets](./field-widgets.md)

```diff
from flask_wtf import FlaskForm
+ from tna_frontend_jinja.wtforms import (
+     TnaEmailInputWidget,
+     TnaTextInputWidget,
+ )
from wtforms import (
    EmailField,
    StringField,
    validators,
)


class TextInputForm(FlaskForm):
    username = StringField(
        "Username",
        description="This will be used to log in",
        validators=[
            validators.InputRequired(message="Enter a username"),
            validators.Length(
                max=32, message="Usernames must be 32 characters or fewer"
            ),
        ],
+         widget=TnaTextInputWidget(),
    )

    email = EmailField(
        "Email address",
        validators=[
            validators.InputRequired(message="Enter an email address"),
            validators.Email(message="Enter a valid email address"),
        ],
+         widget=TnaEmailInputWidget(),
    )

    submit = SubmitField(
        "Continue",
+         widget=TnaSubmitWidget(),
    )
```

## 4. Routing

Create a route to display your form and accept `POST` requests and another route to handle the success state.

This allows us to use the [Post/Redirect/Get pattern](https://en.wikipedia.org/wiki/Post/Redirect/Get).

```python
@app.route("/my-form/", methods=["GET", "POST"])
def my_form():
    form = MyForm()
    if form.validate_on_submit():
        return redirect(url_for("success"))
    return render_template("my-form.html", form=form)

@app.route("/success/")
def success():
    return render_template("success.html")
```

## 5. Templates

```jinja2
{# my-form.html #}

{%- from 'components/error-summary/macro.html' import tnaErrorSummary -%}

{% if form.errors %}
  {{ tnaErrorSummary(wtforms_errors(form)) }}
{% endif %}

<h1 class="tna-heading-xl">My form</h1>

<form action="{{ url_for('my_form') }}" method="post" novalidate>
  {{ form.csrf_token }}

  {{ form.username }}

  {{ form.email }}

  <div class="tna-button-group">
    {{ form.submit }}
  </div>
</form>
```
