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
        self, label=None, validators=None, invalid_date_error_message="", **kwargs
    ):
        super().__init__(label, validators, **kwargs)
        self.format = ["%d %m %Y", "%d %m %y"]
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
            "y": "year",
        }
        return [
            (
                format_parts_full.get(part.replace("%", "").lower(), "")
                if full_code
                else part.replace("%", "").lower()
            )
            for part in self.format[len(self.format) - 1].split(" ")
        ]

    def process(self, formdata, data=unset_value, extra_filters=None):
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
            self.raw_data = [
                formdata.get(
                    f"{self.name}-{part}",
                    "",
                )
                for part in self.field_codes(True)
            ]

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

        date_str = " ".join([value for value in valuelist if value])
        for format in self.strptime_format:
            try:
                self.data = datetime.datetime.strptime(date_str, format).date()
                return
            except ValueError:
                self.data = None

        raise ValueError(self.gettext(self.invalid_date_error_message))


class TnaMonthField(TnaDateField):
    def __init__(self, label=None, validators=None, **kwargs):
        super().__init__(label, validators, **kwargs)
        self.format = ["%m %Y", "%m %y"]
        self.strptime_format = clean_datetime_format_for_strptime(self.format)


class TnaYearField(TnaDateField):
    def __init__(self, label=None, validators=None, **kwargs):
        super().__init__(label, validators, **kwargs)
        self.format = ["%Y", "%y"]
        self.strptime_format = clean_datetime_format_for_strptime(self.format)


class TnaProgressiveDateField(TnaDateField):
    def __init__(self, label=None, validators=None, **kwargs):
        super().__init__(label, validators, **kwargs)
        self.format = ["%Y", "%y", "%Y %m", "%y %m", "%Y %m %d", "%y %m %d"]
        self.progressive = True
        self.strptime_format = clean_datetime_format_for_strptime(self.format)
