from django.forms.forms import BaseForm, DeclarativeFieldsMetaclass
from tna_frontend_jinja.djangoforms.renderers import Jinja2


class TnaForm(BaseForm, metaclass=DeclarativeFieldsMetaclass):
    default_renderer = Jinja2()
