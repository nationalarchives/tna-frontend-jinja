import unittest

from flask_wtf import FlaskForm
from werkzeug.datastructures import MultiDict
from wtforms import (
    StringField,
    validators,
)

from app import app


class TextInputForm(FlaskForm):
    class Meta:
        csrf = False

    string = StringField(
        validators=[],
    )


class TestTextInput(unittest.TestCase):
    def test_empty_form(self):
        error_message = "Enter a username"
        with app.test_request_context():
            form = TextInputForm()
            form.string.validators = [
                validators.InputRequired(message=error_message)
            ]
            complete = form.validate()
            assert form.errors == {"string": [error_message]}
            assert complete is False

    def test_with_data(self):
        error_message = "Enter a username"
        with app.test_request_context():
            formdata = MultiDict([("string", "testuser")])
            form = TextInputForm(formdata=formdata)
            form.string.validators = [
                validators.InputRequired(message=error_message)
            ]
            complete = form.validate()
            assert form.errors == {}
            assert complete is True

            data = {"string": "testuser"}
            form = TextInputForm(formdata=None, data=data)
            form.string.validators = [
                validators.DataRequired(message=error_message)
            ]
            complete = form.validate()
            assert form.errors == {}
            assert complete is True

    def test_with_data_length_validation(self):
        error_message = "Usernames must be 256 characters or fewer"
        with app.test_request_context():
            formdata = MultiDict([("string", "x" * 257)])
            form = TextInputForm(formdata=formdata)
            form.string.validators = [
                validators.Length(max=256, message=error_message)
            ]
            complete = form.validate()
            assert form.errors == {"string": [error_message]}
            assert complete is False

            data = {"string": "x" * 257}
            form = TextInputForm(data=data)
            form.string.validators = [
                validators.Length(max=256, message=error_message)
            ]
            complete = form.validate()
            assert form.errors == {"string": [error_message]}
            assert complete is False
