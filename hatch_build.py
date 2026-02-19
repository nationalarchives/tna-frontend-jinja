import os
import tempfile

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomBuildHook(BuildHookInterface):
    PLUGIN_NAME = "email_css_compiler"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__temp_dir = None

    @property
    def temp_dir(self):
        if self.__temp_dir is None:
            self.__temp_dir = os.path.realpath(tempfile.mkdtemp())

        return self.__temp_dir

    def initialize(self, version, build_data):
        """
        This occurs immediately before each build.

        Any modifications to the build data will be seen by the build target.
        """
        if self.target_name != "sdist":
            return

        print("* Adding compiled email CSS to template (build hook)...")

        compiled_css_path = os.path.join(
            "node_modules",
            "@nationalarchives",
            "frontend",
            "nationalarchives",
            "email.css",
        )
        try:
            with open(
                os.path.join(self.root, compiled_css_path),
                "r",
                encoding="utf-8-sig",
            ) as f:
                compiled_css = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Compiled CSS file not found at {compiled_css_path}. Please ensure npm packages have been installed."
            )
        compiled_css = compiled_css.replace(
            "/*# sourceMappingURL=email.css.map */", ""
        ).strip()

        file_name = "email.html"
        destination = os.path.join(
            "tna_frontend_jinja", "templates", "layouts", file_name
        )
        with open(
            os.path.join(self.root, destination), "r", encoding="utf-8"
        ) as f:
            email_template_content = f.read()
        email_template_content = email_template_content.replace(
            "<!-- COMPILED_EMAIL_CSS -->",
            f'<style media="all" type="text/css">{compiled_css}</style>',
        )

        new_email_template = os.path.join(self.temp_dir, file_name)
        with open(new_email_template, "w", encoding="utf-8") as f:
            f.write(email_template_content)

        if version == "editable":
            build_data["force_include_editable"][
                new_email_template
            ] = destination
        else:
            build_data["force_include"][new_email_template] = destination
