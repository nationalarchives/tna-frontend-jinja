from deepmerge import Merger
from flask import render_template
from markupsafe import Markup
from wtforms.widgets.core import (
    FileInput,
    Input,
    PasswordInput,
    Select,
    SubmitInput,
    TextArea,
    TextInput,
)


def wtforms_errors(form, params={}):
    wtforms_params = {"title": "There is a problem", "items": []}

    id_map = {}
    for field_name in form._fields.keys():
        field = getattr(form, field_name, None)
        if field and hasattr(field, "id"):
            id_map[field_name] = field.id

    wtforms_params["items"] = flatten_errors(form.errors, id_map=id_map)

    return merger.merge(wtforms_params, params)


class WTFormsHelpers(object):
    """WTForms helpers

    Register some template helpers to allow developers to
    map WTForms elements to the GOV.UK jinja macros
    """

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.add_template_global(wtforms_errors)


def flatten_errors(errors, prefix="", id_map={}):
    """Return list of errors from form errors."""
    error_list = []
    if isinstance(errors, dict):
        for key, value in errors.items():
            # Recurse to handle subforms.
            if key in id_map:
                key = id_map[key]
            error_list += flatten_errors(
                value, prefix=f"{prefix}{key}-", id_map=id_map
            )
    elif isinstance(errors, list) and isinstance(errors[0], dict):
        for idx, error in enumerate(errors):
            error_list += flatten_errors(
                error, prefix=f"{prefix}{idx}-", id_map=id_map
            )
    elif isinstance(errors, list):
        error_list.append(
            {"text": errors[0], "href": "#{}".format(prefix.rstrip("-"))}
        )
    else:
        error_list.append(
            {"text": errors, "href": "#{}".format(prefix.rstrip("-"))}
        )
    return error_list


merger = Merger(
    # pass in a list of tuple, with the
    # strategies you are looking to apply
    # to each type.
    [(list, ["append"]), (dict, ["merge"])],
    # next, choose the fallback strategies,
    # applied to all other types:
    ["override"],
    # finally, choose the strategies in
    # the case where the types conflict:
    ["override"],
)


class GovFormBase(object):
    """Collection of helpers

    These are mixed into the WTForms classes which we are subclassing
    to provide extra functionality.

    Some of our subclasses then extend these base utilities for their
    specific use cases
    """

    def __call__(self, field, **kwargs):
        return self.render(self.map_gov_params(field, **kwargs))

    def map_gov_params(self, field, **kwargs):
        """Map WTForms' html params to govuk macros

        Taking WTForms' output, we need to map it to a params dict
        which matches the structure that the govuk macros are expecting
        """
        params = {
            "id": kwargs["id"],
            "name": field.name,
            "label": field.label,
            "attributes": {},
            "hint": field.description or None,
        }

        if "value" in kwargs:
            params["value"] = kwargs["value"]
            del kwargs["value"]

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
            params["errorMessage"] = {"text": field.errors[0]}

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


class GovIterableBase(GovFormBase):
    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)

        if "required" not in kwargs and "required" in getattr(
            field, "flags", []
        ):
            kwargs["required"] = True

        kwargs["items"] = []

        # This field is constructed as an iterable of subfields
        for subfield in field:
            item = {"text": subfield.label.text, "value": subfield._value()}

            if getattr(subfield, "checked", subfield.data):
                item["checked"] = True

            kwargs["items"].append(item)

        return super().__call__(field, **kwargs)

    def map_gov_params(self, field, **kwargs):
        """Completely override the params mapping for this input type

        It bears little resemblance to that of a normal field
        because these fields are effectively collections of
        fields wrapped in an iterable
        """

        params = {
            "name": field.name,
            "items": kwargs["items"],
            "hint": field.description,
        }

        # Merge in any extra params passed in from the template layer
        if "params" in kwargs:
            # Merge items individually as otherwise the merge will append new ones
            if "items" in kwargs["params"]:
                for index, item in enumerate(kwargs["params"]["items"]):
                    item = self.merge_params(params["items"][index], item)

                del kwargs["params"]["items"]

            params = self.merge_params(params, kwargs["params"])

        if field.errors:
            params["errorMessage"] = {"text": field.errors[0]}

        return params


# from govuk_frontend_wtf.gov_form_base import GovFormBase, GovIterableBase

"""Lifted from WTForms and modified to generate GOV.UK markup

The upstream code should be monitored when updating WTForms to
see if any modifications need to be brought in
"""


class GovInput(GovFormBase, Input):
    """Render a basic ``<input>`` field.

    This is used as the basis for most of the other input fields.

    By default, the `_value()` method will be called upon the associated field
    to provide the ``value=`` HTML attribute.
    """

    template = "wtforms/text-input.html"

    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        kwargs.setdefault("type", self.input_type)
        if "value" not in kwargs:
            kwargs["value"] = field._value()
        if "required" not in kwargs and "required" in getattr(
            field, "flags", []
        ):
            kwargs["required"] = True

        return super().__call__(field, **kwargs)


class GovTextInput(GovInput, TextInput):
    """Render a single-line text input."""

    input_type = "text"


class GovSubmitInput(GovInput, SubmitInput):
    """Renders a submit button.

    The field's label is used as the text of the submit button instead of the
    data on the field.
    """

    template = "wtforms/button.html"

    def __call__(self, field, **kwargs):
        return super().__call__(field, **kwargs)

    def map_gov_params(self, field, **kwargs):
        params = super().map_gov_params(field, **kwargs)

        params.setdefault("text", field.label.text)
        params.setdefault("buttonElement", True)
        params.setdefault("buttonType", "submit")

        return params
