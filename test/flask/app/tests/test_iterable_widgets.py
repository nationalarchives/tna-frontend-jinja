import unittest
from types import SimpleNamespace
from unittest.mock import patch

from flask import Flask
from jinja2 import PackageLoader
from wtforms import BooleanField, Form, RadioField, SelectChoice, SelectMultipleField

from tna_frontend_jinja.wtforms import (
    TnaCheckboxesWidget,
    TnaCheckboxWidget,
    TnaRadiosWidget,
)


class TestIterableWidgets(unittest.TestCase):
    field_widgets = (
        (RadioField, TnaRadiosWidget),
        (SelectMultipleField, TnaCheckboxesWidget),
    )

    def test_choice_iterables(self):
        attributes = {"hint": "First hint", "attributes": {"disabled": True}}
        choice_formats = [
            ("legacy tuples", [("1", "First", True), ("2", "Second", False)]),
            (
                "tuples",
                [("1", "First", True, attributes), ("2", "Second", False, {})],
            ),
            (
                "choice objects",
                [
                    SimpleNamespace(
                        value="1", label="First", selected=True, render_kw=attributes
                    ),
                    SimpleNamespace(
                        value="2", label="Second", selected=False, render_kw={}
                    ),
                ],
            ),
            ("empty", []),
        ]
        iterable_types = (
            list,
            tuple,
            iter,
            lambda choices: (choice for choice in choices),
        )
        for field_type, widget_type in self.field_widgets:
            for choice_name, choices in choice_formats:
                for make_iterable in iterable_types:
                    with self.subTest(
                        field=field_type.__name__,
                        choices=choice_name,
                        iterable=make_iterable.__name__,
                    ):

                        class ChoiceForm(Form):
                            choice = field_type(choices=[])

                        form = ChoiceForm()
                        widget = widget_type()
                        with (
                            patch.object(
                                form.choice,
                                "iter_choices",
                                return_value=make_iterable(choices),
                            ),
                            patch.object(widget, "render", side_effect=lambda p: p),
                        ):
                            params = widget(form.choice)

                        expected = []
                        if choices:
                            expected = [
                                {"text": "First", "value": "1", "checked": True},
                                {"text": "Second", "value": "2"},
                            ]
                            if choice_name != "legacy tuples":
                                expected[0].update(attributes)
                        assert params["items"] == expected
                        assert params["selected"] == ("1" if choices else None)
                        assert form.choice.choices == []

    def test_rendering_preserves_choices_and_attributes(self):
        app = Flask(__name__)
        app.jinja_loader = PackageLoader("tna_frontend_jinja")
        choices = [
            (1, "First", {"hint": "First hint", "id": "custom-first"}),
            (2, "Second"),
        ]
        choice_formats = [
            ("tuples", choices),
            ("SelectChoice", [SelectChoice(*choice) for choice in choices]),
        ]

        for field_type, widget_type in self.field_widgets:
            for choice_name, field_choices in choice_formats:
                with self.subTest(field=field_type.__name__, choices=choice_name):

                    class ChoiceForm(Form):
                        choice = field_type(
                            choices=field_choices, coerce=int, widget=widget_type()
                        )

                    data = [1] if field_type is SelectMultipleField else 1
                    form = ChoiceForm(data={"choice": data})
                    original_choices = form.choice.choices
                    with app.app_context():
                        first = str(form.choice())
                        second = str(form.choice())

                    assert first == second
                    assert "First hint" in first
                    assert 'id="custom-first"' in first
                    assert "checked" in first
                    assert 'value="1"' in first
                    assert 'value="2"' in first
                    assert form.choice.choices is original_choices
                    assert form.validate()

    def test_select_choice_options_and_selection(self):
        for field_type, widget_type in self.field_widgets:
            selections = (
                ([], ["first"], ["second"], ["first", "second"])
                if field_type is SelectMultipleField
                else (None, "first", "second")
            )
            for data in selections:
                with self.subTest(field=field_type.__name__, data=data):
                    choices = [
                        SelectChoice(
                            "first",
                            "First",
                            render_kw={"hint": "First hint", "id": "custom-first"},
                        ),
                        SelectChoice("second"),
                    ]

                    class ChoiceForm(Form):
                        choice = field_type(choices=choices, widget=widget_type())

                    form = ChoiceForm(data={"choice": data})
                    valid_before_render = form.validate()
                    errors_before_render = form.errors
                    selected = data if isinstance(data, list) else [data]
                    expected = [
                        {
                            "text": "First",
                            "value": "first",
                            "hint": "First hint",
                            "id": "custom-first",
                        },
                        {"text": "second", "value": "second"},
                    ]
                    for item in expected:
                        if item["value"] in selected:
                            item["checked"] = True

                    with patch.object(
                        form.choice.widget, "render", side_effect=lambda p: p
                    ):
                        for _ in range(2):
                            params = form.choice()
                            assert params["items"] == expected
                            assert params["selected"] == next(
                                (
                                    item["value"]
                                    for item in reversed(expected)
                                    if item.get("checked")
                                ),
                                None,
                            )

                    assert len(form.choice.choices) == len(choices)
                    assert all(
                        original is current
                        for original, current in zip(
                            choices, form.choice.choices, strict=False
                        )
                    )
                    assert form.validate() == valid_before_render
                    assert form.errors == errors_before_render

    def test_single_checkbox(self):
        class CheckboxForm(Form):
            choice = BooleanField(widget=TnaCheckboxWidget())

        form = CheckboxForm(data={"choice": True})
        with patch.object(form.choice.widget, "render", side_effect=lambda p: p):
            params = form.choice()
        assert params["items"] == [{"text": "Choice", "value": "y", "checked": True}]
