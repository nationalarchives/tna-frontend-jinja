import unittest

from app.forms.forms import TextInputForm
from werkzeug.datastructures import MultiDict

from app import app


class TestTextInputForm(unittest.TestCase):
    def setUp(self):
        app.config["WTF_CSRF_ENABLED"] = False

    def test_empty_form(self):
        with app.test_request_context():
            form = TextInputForm()
            assert "Username" in form.field.label.text
            complete = form.validate()
            assert form.errors == {"field": ["Enter a username"]}
            assert complete is False

    def test_with_formdata(self):
        with app.test_request_context():
            formdata = MultiDict([("field", "testuser")])
            form = TextInputForm(formdata=formdata)
            complete = form.validate()
            assert form.errors == {}
            assert complete is True

    def test_with_formdata_too_long(self):
        with app.test_request_context():
            formdata = MultiDict([("field", "x" * 257)])
            form = TextInputForm(formdata=formdata)
            complete = form.validate()
            assert form.errors == {
                "field": ["Usernames must be 256 characters or fewer"]
            }
            assert complete is False

    def test_with_data(self):
        with app.test_request_context():
            data = {"field": "testuser"}
            form = TextInputForm(formdata=None, data=data)
            input_required_validator = [
                i
                for i, v in enumerate(form.field.validators)
                if v.__class__.__name__ == "InputRequired"
            ]
            if input_required_validator:
                form.field.validators.pop(input_required_validator[0])
            complete = form.validate()
            assert form.errors == {}
            assert complete is True
