from deepmerge import Merger

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


def flatten_errors(errors, prefix="", id_map={}):
    """Return list of errors from form errors."""
    error_list = []
    if isinstance(errors, dict):
        for key, value in errors.items():
            # Recurse to handle subforms.
            if key in id_map:
                key = id_map[key]
            error_list += flatten_errors(value, prefix=f"{prefix}{key}-", id_map=id_map)
    elif isinstance(errors, list) and isinstance(errors[0], dict):
        for idx, error in enumerate(errors):
            error_list += flatten_errors(error, prefix=f"{prefix}{idx}-", id_map=id_map)
    elif isinstance(errors, list):
        error_list.append({"text": errors[0], "href": "#{}".format(prefix.rstrip("-"))})
    else:
        error_list.append({"text": errors, "href": "#{}".format(prefix.rstrip("-"))})
    return error_list


def wtforms_errors(form, params={}):
    wtforms_params = {"title": "There is a problem", "items": []}

    id_map = {}
    for field_name in form._fields.keys():
        field = getattr(form, field_name, None)
        if field and hasattr(field, "id"):
            if field.type in ["SelectMultipleField", "RadioField"] and hasattr(
                field, "choices"
            ):
                id_map[field_name] = f"{field.id}-{field.choices[0][0]}"
            elif field.type in [
                "TnaDateField",
                "TnaMonthField",
                "TnaYearField",
                "TnaProgressiveDateField",
            ]:
                id_map[field_name] = (
                    f"{field.id}-{'m' if field.field_codes(True)[0] in ['m', 'b'] else field.field_codes(True)[0]}"
                )
            elif field.type in ["BooleanField"]:
                id_map[field_name] = f"{field.id}-y"
            else:
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
