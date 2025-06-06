import os
from pathlib import Path
from sysconfig import get_path

from django.conf import settings
from django.forms.renderers import BaseRenderer
from django.utils.functional import cached_property


class Jinja2(BaseRenderer):
    """
    Load Jinja2 templates from the built-in widget templates in
    django/forms/jinja2 and from apps' 'jinja2' directory.
    """

    def get_template(self, template_name):
        return self.engine.get_template(template_name)

    def render(self, template_name, context, request=None):
        template = self.get_template(template_name)
        return template.render(context={"params": context}, request=request).strip()

    @cached_property
    def engine(self):
        jinja_config = next(
            template_config
            for template_config in settings.TEMPLATES
            if template_config["BACKEND"] == "django.template.backends.jinja2.Jinja2"
        )
        return self.backend(
            {
                "APP_DIRS": True,
                "DIRS": jinja_config.get("DIRS", [])
                + [
                    os.path.join(Path(__file__).parent.parent, "templates"),
                    os.path.join(get_path("platlib"), "django/forms/templates"),
                ],
                "NAME": "jinja2",
                "OPTIONS": {},
            }
        )

    @cached_property
    def backend(self):
        from django.template.backends.jinja2 import Jinja2

        return Jinja2
