from flask import render_template
from markupsafe import Markup
from wtforms.widgets.core import (
    Input,
    Select,
    TextArea,
    TextInput,
)

from .helpers import merger


class TnaWidget(object):
    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", kwargs["id"] if "id" in kwargs else field.id)
        kwargs.setdefault("name", field.name)
        kwargs.setdefault("headingLevel", 2)
        kwargs.setdefault("label", field.label.text)
        kwargs.setdefault("hint", field.description or None)
        return self.render(self.map_tna_params(field, **kwargs))

    def map_tna_params(self, field, **kwargs):
        params = {
            "id": kwargs["id"],
            "name": kwargs["name"],
            "headingLevel": kwargs["headingLevel"],
            "label": kwargs["label"],
        }

        if "hint" in kwargs:
            params["hint"] = kwargs.get("hint", field.description)

        if "params" in kwargs:
            params.update(kwargs["params"])

        if "type" in kwargs:
            params["type"] = kwargs["type"]

        if field.errors:
            params["error"] = {"text": field.errors[0]}

        if "attributes" in kwargs:
            params["attributes"].update(kwargs["attributes"])

        if "attributes" in params:
            for key, value in params["attributes"].items():
                if value is True:
                    params["attributes"][key] = ""

        return params

    def merge_params(self, a, b):
        return merger.merge(a, b)

    def render(self, params):
        return Markup(render_template(self.template, params=params))


class TnaIterableWidget(TnaWidget):
    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)

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

            params.update(kwargs["params"])

        if field.errors:
            params["error"] = {"text": field.errors[0]}

        return params


class TnaInput(TnaWidget, Input):
    template = "widgets/text-input.html"

    def map_tna_params(self, field, **kwargs):
        params = super().map_tna_params(field, **kwargs)

        if "value" not in params:
            if "value" in kwargs:
                params["value"] = kwargs["value"]
                # del kwargs["value"]
            elif field.data:
                params["value"] = field.data

        return params


class TnaTextInputWidget(TnaInput, TextInput):
    input_type = "text"


class TnaCheckboxesWidget(TnaIterableWidget):
    template = "widgets/checkboxes.html"

    def map_tna_params(self, field, **kwargs):
        params = super().map_tna_params(field, **kwargs)

        params.setdefault(
            "label",
            field.label.text,
        )
        return params


class TnaCheckboxWidget(TnaCheckboxesWidget):
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


class TnaRadiosWidget(TnaIterableWidget):
    template = "widgets/radios.html"
    input_type = "radio"

    def map_tna_params(self, field, **kwargs):
        params = super().map_tna_params(field, **kwargs)
        params.setdefault(
            "label",
            field.label.text,
        )
        return params


class TnaDateInput(TnaWidget):
    template = "widgets/date-input.html"

    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        if "value" not in kwargs:
            kwargs["value"] = field._value()
        return super().__call__(field, **kwargs)

    def map_tna_params(self, field, **kwargs):
        params = super().map_tna_params(field, **kwargs)
        day, month, year = [""] * 3

        if field.raw_data:
            for format_part_index, format_part in enumerate(
                field.format[len(field.format) - 1].split(" ")
            ):
                if format_part.replace("%", "").lower() == "d":
                    day = (
                        field.raw_data[format_part_index]
                        if len(field.raw_data) > format_part_index
                        else ""
                    )
                elif format_part.replace("%", "").lower() in ["m", "b"]:
                    month = (
                        field.raw_data[format_part_index]
                        if len(field.raw_data) > format_part_index
                        else ""
                    )
                elif format_part.replace("%", "").lower() == "y":
                    year = (
                        field.raw_data[format_part_index]
                        if len(field.raw_data) > format_part_index
                        else ""
                    )

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
        params.setdefault("progressive", field.progressive)
        return params


class TnaSubmitWidget(TnaInput):
    template = "widgets/button.html"

    def map_tna_params(self, field, **kwargs):
        params = super().map_tna_params(field, **kwargs)

        params.setdefault("text", field.label.text)
        params.setdefault("buttonElement", True)
        params.setdefault("buttonType", "submit")

        return params


class TnaTextareaWidget(TnaInput, TextArea):
    template = "widgets/textarea.html"

    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        if "value" not in kwargs:
            kwargs["value"] = field._value()
        return super().__call__(field, **kwargs)


class TnaSelectWidget(TnaWidget, Select):
    template = "widgets/select.html"

    def __call__(self, field, **kwargs):
        if self.multiple:
            raise Exception(
                "Please do not render mutliselect elements as a select box"
                " - you should use checkboxes instead in order to comply with"
                " the GOV.UK service manual"
            )

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


class TnaPasswordWidget(TnaTextInputWidget):
    def map_tna_params(self, field, **kwargs):
        params = super().map_tna_params(field, **kwargs)

        params["password"] = True

        return params


class TnaNumberInputWidget(TnaTextInputWidget):
    def map_tna_params(self, field, **kwargs):
        params = super().map_tna_params(field, **kwargs)

        params["inputmode"] = "numeric"

        return params


class TnaEmailInputWidget(TnaTextInputWidget):
    def map_tna_params(self, field, **kwargs):
        params = super().map_tna_params(field, **kwargs)

        params["inputmode"] = "email"

        return params


class TnaTelInputWidget(TnaTextInputWidget):
    def map_tna_params(self, field, **kwargs):
        params = super().map_tna_params(field, **kwargs)

        params["inputmode"] = "tel"

        return params


class TnaUrlInputWidget(TnaTextInputWidget):
    def map_tna_params(self, field, **kwargs):
        params = super().map_tna_params(field, **kwargs)

        params["inputmode"] = "url"

        return params


class TnaSearchFieldWidget(TnaTextInputWidget):
    template = "widgets/search-field.html"

    def map_tna_params(self, field, **kwargs):
        params = super().map_tna_params(field, **kwargs)
        print(f"params: {params}")
        print(f"kwargs: {kwargs}")
        return params
