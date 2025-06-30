import datetime
import itertools

from wtforms.fields.datetime import DateField
from wtforms.utils import clean_datetime_format_for_strptime, unset_value

from ..widgets import TnaDateInput


class TnaDateField(DateField):
    """
    A text field which stores a :class:`datetime.datetime` matching one or
    several formats. If ``format`` is a list, any input value matching any
    format will be accepted, and the first format in the list will be used
    to produce HTML values.
    """

    widget = TnaDateInput()

    def __init__(
        self,
        label=None,
        validators=None,
        allow_two_digit_year=False,
        invalid_date_error_message="",
        **kwargs,
    ):
        super().__init__(label, validators, **kwargs)
        self.format = [
            format
            for format in [
                "%d %m %Y",
                ("%d %m %y") if allow_two_digit_year else None,
                "%d %b %Y",
                ("%d %b %y") if allow_two_digit_year else None,
                "%d %B %Y",
                ("%d %B %y") if allow_two_digit_year else None,
            ]
            if format is not None
        ]
        self.progressive = False
        self.strptime_format = clean_datetime_format_for_strptime(self.format)
        if invalid_date_error_message:
            self.invalid_date_error_message = invalid_date_error_message
        else:
            self.invalid_date_error_message = self.gettext(
                f"{self.label.text} must be a real date"
            )

    def field_codes(self, full_code=False):
        """
        Return a list of field names that this field encapsulates.
        This is used by the TnaDateInput widget to render the date inputs.
        """
        format_parts_full = {
            "d": "day",
            "m": "month",
            "b": "month",
            "y": "year",
        }
        return [
            (
                format_parts_full.get(part.replace("%", "").lower(), "")
                if full_code
                else (
                    "m"
                    if part.replace("%", "").lower() in ["m", "b"]
                    else part.replace("%", "").lower()
                )
            )
            for part in self.format[len(self.format) - 1].split(" ")
        ]

    def process(self, formdata, data=unset_value, extra_filters=None):  # noqa: C901
        """
        Process incoming data, calling process_data, process_formdata as needed,
        and run filters.

        If `data` is not provided, process_data will be called on the field's
        default.

        Field subclasses usually won't override this, instead overriding the
        process_formdata and process_data methods. Only override this for
        special advanced processing, such as when a field encapsulates many
        inputs.

        :param extra_filters: A sequence of extra filters to run.
        """
        self.process_errors = []
        if data is unset_value:
            try:
                data = self.default()
            except TypeError:
                data = self.default

        self.object_data = data

        try:
            self.process_data(data)
        except ValueError as e:
            self.process_errors.append(e.args[0])

        if formdata is not None:
            raw_data = [
                formdata.get(
                    f"{self.name}-{part}",
                    "",
                )
                for part in self.field_codes(True)
            ]

            if "" in raw_data:
                raw_data = raw_data[: raw_data.index("")]

            self.raw_data = raw_data

            try:
                self.process_formdata(self.raw_data)
            except ValueError as e:
                self.process_errors.append(e.args[0])

        try:
            for filter in itertools.chain(self.filters, extra_filters or []):
                self.data = filter(self.data)
        except ValueError as e:
            self.process_errors.append(e.args[0])

    def process_formdata(self, valuelist):
        if not valuelist:
            return

        if "" in valuelist:
            valuelist = valuelist[: valuelist.index("")]

        date_str = " ".join([value for value in valuelist if value])
        for format in self.strptime_format:
            try:
                self.data = datetime.datetime.strptime(date_str, format).date()
                return
            except ValueError:
                self.data = None

        raise ValueError(self.gettext(self.invalid_date_error_message))


class TnaMonthField(TnaDateField):
    def __init__(
        self, label=None, validators=None, allow_two_digit_year=False, **kwargs
    ):
        super().__init__(label, validators, **kwargs)
        self.format = [
            format
            for format in [
                "%m %Y",
                ("%m %y") if allow_two_digit_year else None,
                "%b %Y",
                ("%b %y") if allow_two_digit_year else None,
                "%B %Y",
                ("%B %y") if allow_two_digit_year else None,
            ]
            if format is not None
        ]
        self.strptime_format = clean_datetime_format_for_strptime(self.format)


class TnaYearField(TnaDateField):
    def __init__(
        self, label=None, validators=None, allow_two_digit_year=False, **kwargs
    ):
        super().__init__(label, validators, **kwargs)
        self.format = [
            format
            for format in ["%Y", ("%y") if allow_two_digit_year else None]
            if format is not None
        ]
        self.strptime_format = clean_datetime_format_for_strptime(self.format)


class TnaProgressiveDateField(TnaDateField):
    def __init__(
        self, label=None, validators=None, allow_two_digit_year=False, **kwargs
    ):
        super().__init__(label, validators, **kwargs)
        self.format = [
            format
            for format in [
                "%Y",
                ("%y") if allow_two_digit_year else None,
                "%Y %m",
                ("%y %m") if allow_two_digit_year else None,
                "%Y %b",
                ("%y %b") if allow_two_digit_year else None,
                "%Y %B",
                ("%y %B") if allow_two_digit_year else None,
                "%Y %m %d",
                ("%y %m %d") if allow_two_digit_year else None,
                "%Y %b %d",
                ("%y %b %d") if allow_two_digit_year else None,
                "%Y %B %d",
                ("%y %B %d") if allow_two_digit_year else None,
            ]
            if format is not None
        ]
        self.progressive = True
        self.strptime_format = clean_datetime_format_for_strptime(self.format)
