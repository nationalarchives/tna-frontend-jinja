from django.forms.widgets import (
    CheckboxInput,
    CheckboxSelectMultiple,
    ClearableFileInput,
    DateInput,
    DateTimeInput,
    EmailInput,
    FileInput,
    HiddenInput,
    Input,
    MultipleHiddenInput,
    NullBooleanSelect,
    NumberInput,
    PasswordInput,
    RadioSelect,
    Select,
    SelectDateWidget,
    SelectMultiple,
    SplitDateTimeWidget,
    SplitHiddenDateTimeWidget,
    Textarea,
    TextInput,
    TimeInput,
    URLInput,
)


class TnaTextInput(TextInput):
    input_type = "text"
    template_name = "components/text-input.html"
