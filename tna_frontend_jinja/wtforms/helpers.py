def flatten_errors(errors, prefix="", id_map={}):
    """Return list of errors from form errors."""
    error_list = []
    if isinstance(errors, dict):
        for key, value in errors.items():
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
            {
                "text": errors[0],
                "href": f"#{prefix.rstrip('-')}",
            }
        )
    else:
        error_list.append(
            {
                "text": errors,
                "href": f"#{prefix.rstrip('-')}",
            }
        )
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
            else:
                id_map[field_name] = field.id

    errors = form.errors
    csrf_errors = errors.pop("csrf_token", None)

    wtforms_params["items"] = flatten_errors(errors, id_map=id_map)

    if csrf_errors:
        wtforms_params["items"].extend(
            [
                {
                    "text": "The form timed out - try submitting again",
                    "href": None,
                }
            ]
        )

    merged = wtforms_params.copy()
    merged.update(params)

    return merged


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
