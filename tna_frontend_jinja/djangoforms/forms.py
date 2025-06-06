from django.forms.forms import BaseForm, DeclarativeFieldsMetaclass
from tna_frontend_jinja.djangoforms.renderers import Jinja2
from django.forms.utils import ErrorList


class TnaForm(BaseForm, metaclass=DeclarativeFieldsMetaclass):
    default_renderer = Jinja2()

    # def __init__(
    #     self,
    #     data=None,
    #     files=None,
    #     auto_id="id_%s",
    #     prefix=None,
    #     initial=None,
    #     error_class=ErrorList,
    #     label_suffix=None,
    #     empty_permitted=False,
    #     field_order=None,
    #     use_required_attribute=None,
    #     renderer=None,
    #     bound_field_class=None,
    # ):
    #     super().__init__(
    #         data=None,
    #         files=None,
    #         auto_id="id_%s",
    #         prefix=None,
    #         initial=None,
    #         error_class=ErrorList,
    #         label_suffix="---------",
    #         empty_permitted=False,
    #         field_order=None,
    #         use_required_attribute=None,
    #         renderer=None,
    #         bound_field_class=None,
    #     )
