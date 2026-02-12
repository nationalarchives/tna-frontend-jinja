from django.forms.widgets import (  # CheckboxInput,; CheckboxSelectMultiple,; ClearableFileInput,; DateInput,; DateTimeInput,; EmailInput,; FileInput,; HiddenInput,; MultipleHiddenInput,; NullBooleanSelect,; NumberInput,; RadioSelect,; Select,; SelectDateWidget,; SelectMultiple,; SplitDateTimeWidget,; SplitHiddenDateTimeWidget,; Textarea,; TimeInput,; URLInput,
    Input,
    PasswordInput,
    TextInput,
)


class TnaInput(Input):

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        return context | {"params": context["widget"]["attrs"]}


class TnaTextInputWidget(TextInput, TnaInput):
    input_type = "text"
    template_name = "widgets/text-input.html"


class TnaPasswordWidget(PasswordInput, TnaTextInputWidget):
    input_type = "password"
