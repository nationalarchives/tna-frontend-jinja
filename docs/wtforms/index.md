# WTForms integration

## Get started

### 1. Installation

```sh
# Install the WTForms version with Poetry
poetry add tna-frontend-jinja[wtforms]

# Install the WTForms version with pip
pip install tna-frontend-jinja[wtforms]
```

The dependencies added for [WTForms](https://wtforms.readthedocs.io/en/3.2.x/) are done through [Flask-WTF](https://flask-wtf.readthedocs.io/en/1.2.x/).

Flask-WTF includes some helpful extras to WTForms, like CSRF and file upload. Both are maintained as part of the [Pallets Ecosystem](https://github.com/pallets-eco).

`tna-frontend-jinja` depends on the `email` version of Flask-WTF so that [email-validator](https://pypi.org/project/email-validator/) is also included, allowing you to validate email addresses.

The dependency chain looks like:

```
tna-frontend-jinja[wtforms]
  ↳ Flask-WTF[email]
    ↳ Flask
    ↳ WTForms
    ↳ email_validator
    ↳ ...
```

### 2. Add the TNA Frontend Jinja WTForms helpers

```py
from flask import Flask
from tna_frontend_jinja.wtforms.helpers import WTFormsHelpers


app = Flask(__name__)
WTFormsHelpers(app)
```

### 3. Form setup

#### 3.1. Create a form with fields

- [Defining a WTForms form](https://wtforms.readthedocs.io/en/3.1.x/forms/#defining-forms)
- [WTForms fields](https://wtforms.readthedocs.io/en/3.1.x/fields/)
- [TNA WTForms fields](./tna-fields.md)

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

#### 3.2. Add some validation

- [WTForms validators](https://wtforms.readthedocs.io/en/3.1.x/validators/#built-in-validators)
- [TNA WTForms validators](./tna-validators.md)

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

#### 3.3. Use the TNA widgets

- [Supported field widgets](#supported-fields-and-widgets)

Use `render_kw` to set defaults for the attributes on the field. These can be overwritten by `params` in the template.

The available options can be found under the "Nunjucks options" dropdown of the Nunjucks examples in the components section of the [National Archives Design System](https://design-system.nationalarchives.gov.uk/components/).

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
+         render_kw={"size": "m"},
    )

    submit = SubmitField(
        "Continue",
+         widget=TnaSubmitWidget(),
    )
```

### 4. Routing

Create a route to display your form and accept `POST` requests and another route to handle the success state.

This allows us to use the [Post/Redirect/Get pattern](https://en.wikipedia.org/wiki/Post/Redirect/Get).

```python
# Accept GET and POST requests
@app.route("/my-form/", methods=["GET", "POST"])
def my_form():
    # Instantiate a form
    form = MyForm()

    # flask_wtf provides a validate_on_submit which runs on POST and runs the validation
    if form.validate_on_submit():
        # Redirect to the success page
        return redirect(url_for("success"))

    # If the request is a GET or validation is not successful, render the form
    return render_template("my-form.html", form=form)

@app.route("/success/")
def success():
    # Render the success/next page
    return render_template("success.html")
```

### 5. Templates

Add a `my-form.html` template to render the form.

Output the form fields in whatever order or structure you need.

Customise the components by adding a `params` parameter to the field constructor. These can be any documented in the [National Archives Design System](https://design-system.nationalarchives.gov.uk/components/) for that component.

```jinja
{%- from 'components/error-summary/macro.html' import tnaErrorSummary -%}

{% if form.errors %}
  {{ tnaErrorSummary(wtforms_errors(form)) }}
{% endif %}

<h1 class="tna-heading-xl">My form</h1>

<form action="{{ url_for('my_form') }}" method="post" novalidate>
  {{ form.csrf_token }}

  <!-- Add the username field -->
  {{ form.username }}

  <!-- Add the email field and customise it with parameters -->
  {{ form.email(params={'headingLevel': 2}) }}

  <div class="tna-button-group">
    {{ form.submit }}
  </div>
</form>
```

## Supported fields and widgets

| WTForms field                                                                                               | TNA widget(s)                                                             |
| ----------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| [`BooleanField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.BooleanField)               | ✅ `TnaCheckboxWidget`                                                    |
| [`ColorField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.ColorField)                   | 🔧 [not yet supported]                                                    |
| [`DateField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.DateField)                     | ❌ [not supported] - use [`TnaDateField`](./tna-fields.md#tnadatefield)   |
| [`DateTimeField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.DateTimeField)             | 🔧 [not yet supported]                                                    |
| [`DateTimeLocalField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.DateTimeLocalField)   | 🔧 [not yet supported]                                                    |
| [`DecimalField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.DecimalField)               | ✅ `TnaNumberInputWidget`                                                 |
| [`DecimalRangeField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.DecimalRangeField)     | 🔧 [not yet supported]                                                    |
| [`EmailField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.EmailField)                   | ✅ `TnaEmailInputWidget`                                                  |
| [`FieldList`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.FieldList)                     | 🔧 [not yet supported]                                                    |
| [`FileField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.FileField)                     | ✅ `TnaFileInputWidget` or `TnaDroppableFileInputWidget`                  |
| [`FloatField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.FloatField)                   | ✅ `TnaNumberInputWidget`                                                 |
| [`FormField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.FormField)                     | ✅ `TnaFieldsetWidget` (optional)                                         |
| [`HiddenField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.HiddenField)                 | ✅ [none needed]                                                          |
| [`IntegerField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.IntegerField)               | ✅ `TnaNumberInputWidget`                                                 |
| [`IntegerRangeField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.IntegerRangeField)     | 🔧 [not yet supported]                                                    |
| [`MultipleFileField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.MultipleFileField)     | ✅ `TnaFilesInputWidget` or `TnaDroppableFilesInputWidget`                |
| [`MonthField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.MonthField)                   | ❌ [not supported] - use [`TnaMonthField`](./tna-fields.md#tnamonthfield) |
| [`PasswordField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.PasswordField)             | ✅ `TnaPasswordWidget`                                                    |
| [`RadioField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.RadioField)                   | ✅ `TnaRadiosWidget`                                                      |
| [`SelectField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.SelectField)                 | ✅ `TnaSelectWidget`                                                      |
| [`SearchField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.SearchField)                 | ✅ `TnaSearchFieldWidget`                                                 |
| [`SelectMultipleField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.SelectMultipleField) | ✅ `TnaCheckboxesWidget`                                                  |
| [`SubmitField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.SubmitField)                 | ✅ `TnaSubmitWidget`                                                      |
| [`StringField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.StringField)                 | ✅ `TnaTextInputWidget`                                                   |
| [`TelField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.TelField)                       | ✅ `TnaTelInputWidget`                                                    |
| [`TimeField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.TimeField)                     | 🔧 [not yet supported]                                                    |
| [`TextAreaField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.TextAreaField)             | ✅ `TnaTextareaWidget`                                                    |
| [`URLField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.URLField)                       | ✅ `TnaUrlInputWidget`                                                    |
