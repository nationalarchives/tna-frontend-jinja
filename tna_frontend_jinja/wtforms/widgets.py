from flask import render_template
from markupsafe import Markup
from wtforms.widgets.core import (
    Input,
    Select,
    TextArea,
    TextInput,
)


class TnaWidget(object):
    """
    Base class for all TNA Frontend WTForms widgets
    """

    allowed_template_params = [
        "label",
        "headingLevel",
        "headingSize",
        "hint",
        "classes",
        "attributes",
        "formItemClasses",
        "formItemAttributes",
    ]

    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", kwargs.get("id", field.id))
        kwargs.setdefault("name", field.name)
        kwargs.setdefault("label", field.label.text)
        kwargs.setdefault("hint", field.description or None)
        return self.render(self.map_tna_params(field, **kwargs))

    def map_tna_params(self, field, **kwargs):
        params = kwargs
        template_params = params.pop("params", {})

        for key in self.allowed_template_params:
            value = None
            if (
                key in template_params
                and isinstance(template_params[key], dict)
                and key in params
                and isinstance(params[key], dict)
            ):
                merged = params[key].copy()
                merged.update(template_params[key])
                value = merged
            if key in template_params:
                value = template_params[key]
            elif key in params:
                value = params[key]

            if value:
                if key in params and isinstance(params[key], dict):
                    params[key].update(value)
                else:
                    params[key] = value

        if isinstance(field.errors, list) and len(field.errors):
            params["error"] = {"text": field.errors[0]}

        for attributes_key in ["attributes", "formItemAttributes"]:
            if attributes_key in params:
                for key, value in params[attributes_key].items():
                    if value is True:
                        params[attributes_key][key] = ""
                    else:
                        params[attributes_key][key] = value

        return params

    def render(self, params):
        return Markup(render_template(self.template, params=params))


class TnaIterableWidget(TnaWidget):
    """
    Base class for widgets that iterate over subfields, like checkboxes, radios and select components
    """

    def __init__(self):
        super().__init__()
        self.allowed_template_params = self.allowed_template_params + [
            "small",
            "inline",
        ]

    def __call__(self, field, **kwargs):
        kwargs["items"] = []
        kwargs["selected"] = None

        for subfield in field:
            item = {"text": subfield.label.text, "value": subfield._value()}

            if getattr(subfield, "checked", subfield.data):
                item["checked"] = True
                kwargs["selected"] = subfield._value()

            kwargs["items"].append(item)

        return super().__call__(field, **kwargs)


class TnaInput(TnaWidget, Input):
    template = "widgets/text-input.html"

    def __init__(self):
        super().__init__()
        self.allowed_template_params = self.allowed_template_params + [
            "type",
            "inputmode",
            "autocomplete",
            "size",
            "maxLength",
        ]

    def map_tna_params(self, field, **kwargs):
        params = super().map_tna_params(field, **kwargs)

        if "value" not in params:
            if "value" in kwargs:
                params["value"] = kwargs["value"]
            elif field.data:
                params["value"] = field.data

        return params


class TnaTextInputWidget(TnaInput, TextInput):
    input_type = "text"

    def __init__(self):
        super().__init__()
        self.allowed_template_params = self.allowed_template_params + [
            "password",
            "spellcheck",
            "autocapitalize",
            "autocorrect",
        ]


class TnaCheckboxesWidget(TnaIterableWidget):
    template = "widgets/checkboxes.html"


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

    def map_tna_params(self, field, **kwargs):
        params = super().map_tna_params(field, **kwargs)

        if description := field.description:
            params["items"][0]["text"] = description
            del params["hint"]

        return params


class TnaRadiosWidget(TnaIterableWidget):
    template = "widgets/radios.html"
    input_type = "radio"


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
        elif field.data:
            day = str(field.data.day).rjust(2, "0")
            month = str(field.data.month).rjust(2, "0")
            year = field.data.year

        params["value"] = {}
        if day:
            params["value"]["day"] = day
        if month:
            params["value"]["month"] = month
        if year:
            params["value"]["year"] = year
        params.setdefault("fields", field.field_codes())
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


class TnaPasswordWidget(TnaTextInputWidget):
    def map_tna_params(self, field, **kwargs):
        params = super().map_tna_params(field, **kwargs)

        params.setdefault("password", True)

        return params


class TnaNumberInputWidget(TnaTextInputWidget):
    def map_tna_params(self, field, **kwargs):
        params = super().map_tna_params(field, **kwargs)

        params.setdefault("inputmode", "numeric")

        return params


class TnaEmailInputWidget(TnaTextInputWidget):
    def map_tna_params(self, field, **kwargs):
        params = super().map_tna_params(field, **kwargs)

        params.setdefault("inputmode", "email")

        return params


class TnaTelInputWidget(TnaTextInputWidget):
    def map_tna_params(self, field, **kwargs):
        params = super().map_tna_params(field, **kwargs)

        params.setdefault("inputmode", "tel")

        return params


class TnaUrlInputWidget(TnaTextInputWidget):
    def map_tna_params(self, field, **kwargs):
        params = super().map_tna_params(field, **kwargs)

        params.setdefault("inputmode", "url")

        return params


class TnaSearchFieldWidget(TnaTextInputWidget):
    template = "widgets/search-field.html"


class TnaFileInputWidget(TnaInput):
    template = "widgets/file-input.html"


class TnaFilesInputWidget(TnaFileInputWidget):
    def map_tna_params(self, field, **kwargs):
        params = super().map_tna_params(field, **kwargs)

        params.setdefault("multiple", True)

        return params


class TnaDroppableFileInputWidget(TnaFileInputWidget):
    def map_tna_params(self, field, **kwargs):
        params = super().map_tna_params(field, **kwargs)

        params.setdefault("droppable", True)

        return params


class TnaDroppableFilesInputWidget(TnaFilesInputWidget):
    def map_tna_params(self, field, **kwargs):
        params = super().map_tna_params(field, **kwargs)

        params.setdefault("multiple", True)
        params.setdefault("droppable", True)

        return params


class TnaFieldsetWidget(TnaWidget):
    template = "widgets/fieldset.html"

    def map_tna_params(self, field, **kwargs):
        params = super().map_tna_params(field, **kwargs)

        params["legend"] = params.get("label", field.label.text)

        params["html"] = ""
        for subfield in field:
            params["html"] += subfield()

        return params
