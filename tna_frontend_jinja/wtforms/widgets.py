from flask import render_template
from markupsafe import Markup
from wtforms.widgets.core import (
    Input,
    PasswordInput,
    Select,
    SubmitInput,
    TextArea,
    TextInput,
)

from .helpers import merger


class TnaFormBase(object):
    """Collection of helpers

    These are mixed into the WTForms classes which we are subclassing
    to provide extra functionality.

    Some of our subclasses then extend these base utilities for their
    specific use cases
    """

    def __call__(self, field, **kwargs):
        return self.render(self.map_tna_params(field, **kwargs))

    def map_tna_params(self, field, **kwargs):
        """Map WTForms' html params to TNA macros

        Taking WTForms' output, we need to map it to a params dict
        which matches the structure that the TNA macros are expecting
        """
        params = {
            "id": kwargs["id"],
            "name": field.name,
            "label": field.label,
            "attributes": {},
            "hint": field.description or None,
        }

        # Not all form elements have a type so guard against it not existing
        if "type" in kwargs:
            params["type"] = kwargs["type"]
            del kwargs["type"]

        # Remove items that we've already used from the kwargs
        del kwargs["id"]

        if "items" in kwargs:
            del kwargs["items"]

        # Merge in any extra params passed in from the template layer
        if "params" in kwargs:
            params = self.merge_params(params, kwargs["params"])

            # And then remove it, to make sure it doesn't make it's way into the attributes below
            del kwargs["params"]

        # Map error messages
        if field.errors:
            params["error"] = {"text": field.errors[0]}

        # And then Merge any remaining attributes directly to the attributes param
        # This catches anything set in the more traditional WTForms manner
        # i.e. directly as kwargs passed into the field when it's rendered
        params["attributes"] = self.merge_params(params["attributes"], kwargs)

        # Map attributes such as required="True" to required="required"
        for key, value in params["attributes"].items():
            if value is True:
                params["attributes"][key] = key

        return params

    def merge_params(self, a, b):
        return merger.merge(a, b)

    def render(self, params):
        return Markup(render_template(self.template, params=params))


class TnaIterableBase(TnaFormBase):
    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)

        if "required" not in kwargs and "required" in getattr(field, "flags", []):
            kwargs["required"] = True

        kwargs["items"] = []
        kwargs["selected"] = None

        for subfield in field:
            item = {"text": subfield.label.text, "value": subfield._value()}

            if getattr(subfield, "checked", subfield.data):
                item["checked"] = True
                kwargs["selected"] = subfield._value()

            kwargs["items"].append(item)

        return super().__call__(field, **kwargs)

    def map_tna_params(self, field, **kwargs):
        params = {
            "id": field.id,
            "name": field.name,
            "items": kwargs["items"],
            "selected": kwargs["selected"],
            "hint": field.description,
        }

        if "params" in kwargs:
            if "items" in kwargs["params"]:
                for index, item in enumerate(kwargs["params"]["items"]):
                    item = self.merge_params(params["items"][index], item)

                del kwargs["params"]["items"]

            params = self.merge_params(params, kwargs["params"])

        if field.errors:
            params["error"] = {"text": field.errors[0]}

        return params


class TnaInput(TnaFormBase, Input):
    """Render a basic `<input>` field.

    This is used as the basis for most of the other input fields.

    By default, the `_value()` method will be called upon the associated field
    to provide the `value=` HTML attribute.
    """

    template = "widgets/text-input.html"

    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        kwargs.setdefault("type", self.input_type)
        if "value" not in kwargs:
            kwargs["value"] = field._value()
        if "required" not in kwargs and "required" in getattr(field, "flags", []):
            kwargs["required"] = True

        return super().__call__(field, **kwargs)

    def map_tna_params(self, field, **kwargs):
        params = super().map_tna_params(field, **kwargs)

        if "value" in kwargs:
            params["value"] = kwargs["value"]
            del kwargs["value"]

        return params


class TnaTextInput(TnaInput, TextInput):
    """Render a single-line text input."""

    input_type = "text"


class TnaPasswordInput(TnaInput, PasswordInput):
    """Render a password input."""

    input_type = "password"

    def map_tna_params(self, field, **kwargs):
        params = super().map_tna_params(field, **kwargs)

        params["password"] = True

        return params


class TnaCheckboxesInput(TnaIterableBase):
    """Multiple checkboxes, from a SelectMultipleField

    This widget type doesn't exist in WTForms - the recommendation
    there is to use a combination of the list and checkbox widgets.
    However in the GOV.UK macros this type of field is not simply
    a list of smaller widgets - multiple checkboxes are a single
    construct of their own.
    """

    template = "widgets/checkboxes.html"
    input_type = "checkbox"

    def map_tna_params(self, field, **kwargs):
        params = super().map_tna_params(field, **kwargs)

        params.setdefault(
            "label",
            field.label.text,
        )
        return params


class TnaCheckboxInput(TnaCheckboxesInput):
    """Render a single checkbox (i.e. a WTForms BooleanField)."""

    def __call__(self, field, **kwargs):
        class IterableField(object):
            def __init__(self, field):
                self.field = field
                self.max = 1

            def __iter__(self):
                self.index = 0
                return self

            def __next__(self):
                if self.index < self.max:
                    self.index += 1

                    return self.field
                else:
                    raise StopIteration

            def __getattr__(self, name):
                return getattr(self.field, name)

        field_group = IterableField(field)

        return super().__call__(field_group, **kwargs)

    def map_tna_params(self, field, **kwargs):
        params = super().map_tna_params(field, **kwargs)
        params["label"] = kwargs["params"].get("label", "")

        return params


class TnaRadioInput(TnaIterableBase):
    """Render radio button inputs.

    Uses the field label as the fieldset legend.
    """

    template = "widgets/radios.html"
    input_type = "radio"

    def map_tna_params(self, field, **kwargs):
        params = super().map_tna_params(field, **kwargs)
        params.setdefault(
            "label",
            field.label.text,
        )
        return params


class TnaDateInput(TnaFormBase):
    """Renders three input fields representing Day, Month and Year.

    To be used as a widget for WTForms' DateField or DateTimeField.
    The input field labels are hardcoded to "Day", "Month" and "Year".
    The provided label is set as a legend above the input fields.
    The field names MUST all be the same for this widget to work.
    """

    template = "widgets/date-input.html"

    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        if "value" not in kwargs:
            kwargs["value"] = field._value()
        if "required" not in kwargs and "required" in getattr(field, "flags", []):
            kwargs["required"] = True
        return super().__call__(field, **kwargs)

    def map_tna_params(self, field, **kwargs):
        params = super().map_tna_params(field, **kwargs)
        day, month, year = [""] * 3

        if field.raw_data:
            for format_part_index, format_part in enumerate(field.format[0].split(" ")):
                if format_part.replace("%", "").lower() == "d":
                    day = field.raw_data[format_part_index]
                elif format_part.replace("%", "").lower() == "m":
                    month = field.raw_data[format_part_index]
                elif format_part.replace("%", "").lower() == "y":
                    year = field.raw_data[format_part_index]

        params["fields"] = field.field_codes()
        params.setdefault("label", field.label.text)
        params.setdefault(
            "value",
            {
                "day": day,
                "month": month,
                "year": year,
            },
        )
        return params


class TnaSubmitInput(TnaInput, SubmitInput):
    """Renders a submit button.

    The field's label is used as the text of the submit button instead of the
    data on the field.
    """

    template = "widgets/button.html"

    def map_tna_params(self, field, **kwargs):
        params = super().map_tna_params(field, **kwargs)

        params.setdefault("text", field.label.text)
        params.setdefault("buttonElement", True)
        params.setdefault("buttonType", "submit")

        return params


class TnaTextArea(TnaFormBase, TextArea):
    """Renders a multi-line text area.

    `rows` and `cols` ought to be passed as keyword args when rendering.
    """

    template = "widgets/textarea.html"

    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        if "value" not in kwargs:
            kwargs["value"] = field._value()
        if "required" not in kwargs and "required" in getattr(field, "flags", []):
            kwargs["required"] = True
        return super().__call__(field, **kwargs)

    def map_tna_params(self, field, **kwargs):
        params = super().map_tna_params(field, **kwargs)

        if "value" in kwargs:
            params["value"] = kwargs["value"]
            del kwargs["value"]

        return params


class TnaSelect(TnaFormBase, Select):
    """Renders a select field.

    If `multiple` is True, then the `size` property should be specified on
    rendering to make the field useful.

    The field must provide an `iter_choices()` method which the widget will
    call on rendering; this method must yield tuples of
    `(value, label, selected)`.
    """

    template = "widgets/select.html"

    def __call__(self, field, **kwargs):
        if self.multiple:
            raise Exception(
                "Please do not render mutliselect elements as a select box"
                " - you should use checkboxes instead in order to comply with"
                " the GOV.UK service manual"
            )

        kwargs.setdefault("id", field.id)

        if "required" not in kwargs and "required" in getattr(field, "flags", []):
            kwargs["required"] = True

        kwargs["items"] = []

        for val, label, selected, render_kw in field.iter_choices():
            item = {"text": label, "value": val, "selected": selected}

            kwargs["items"].append(item)

            if selected:
                kwargs["selected"] = val

        return super().__call__(field, **kwargs)

    def map_tna_params(self, field, **kwargs):
        params = super().map_tna_params(field, **kwargs)

        params["items"] = kwargs["items"]

        if "selected" in kwargs:
            params["selected"] = kwargs["selected"]
            del kwargs["selected"]

        return params
