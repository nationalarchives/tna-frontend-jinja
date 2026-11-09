import unittest
from types import SimpleNamespace
from unittest.mock import patch

from wtforms import Form, RadioField, SelectMultipleField, StringField

from tna_frontend_jinja.wtforms import (
    TnaDateField,
    TnaMonthField,
    TnaProgressiveDateField,
    TnaYearField,
)
from tna_frontend_jinja.wtforms.helpers import wtforms_errors


class TestWTFormsErrors(unittest.TestCase):
    def test_date_error_anchors(self):
        for field_type in (
            TnaDateField,
            TnaMonthField,
            TnaYearField,
            TnaProgressiveDateField,
        ):

            class DateForm(Form):
                date = field_type(id="custom-date")

            form = DateForm(prefix="form-")
            parts = form.date.field_codes(True)
            for invalid_parts in ([], *([part] for part in parts), parts):
                with self.subTest(
                    field=field_type.__name__, invalid_parts=invalid_parts
                ):
                    form.date.invalid_parts = invalid_parts
                    form.date.errors = ["Enter a valid date"]
                    part = invalid_parts[0] if invalid_parts else parts[0]
                    assert wtforms_errors(form)["items"] == [
                        {"text": "Enter a valid date", "href": f"#custom-date-{part}"}
                    ]

    def test_choice_iterables(self):
        choice_formats = [
            ("legacy tuples", [("first", "First", False)]),
            ("tuples", [("first", "First", False, {})]),
            ("choice objects", [SimpleNamespace(value="first")]),
            ("empty", []),
        ]
        iterable_types = [
            ("list", list),
            ("tuple", tuple),
            ("iterator", iter),
            ("generator", lambda choices: (choice for choice in choices)),
        ]
        for field_type in (RadioField, SelectMultipleField):
            for choice_name, choices in choice_formats:
                for iterable_name, make_iterable in iterable_types:
                    with self.subTest(
                        field=field_type.__name__,
                        choices=choice_name,
                        iterable=iterable_name,
                    ):

                        class ChoiceForm(Form):
                            choice = field_type(choices=[])

                        form = ChoiceForm(prefix="form-")
                        form.choice.errors = ["Choose an option"]
                        with patch.object(
                            form.choice,
                            "iter_choices",
                            return_value=make_iterable(choices),
                        ):
                            summary = wtforms_errors(form)

                        anchor = "#form-choice-first" if choices else "#form-choice"
                        assert summary == {
                            "title": "There is a problem",
                            "items": [{"text": "Choose an option", "href": anchor}],
                        }

    def test_other_fields_and_parameter_overrides(self):
        class TextForm(Form):
            text = StringField(id="custom-text")

        form = TextForm()
        form.text.errors = ["Enter some text"]

        assert wtforms_errors(form, {"title": "Check your answers"}) == {
            "title": "Check your answers",
            "items": [{"text": "Enter some text", "href": "#custom-text"}],
        }
