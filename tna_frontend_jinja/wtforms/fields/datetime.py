import calendar
import itertools
from datetime import UTC, date, datetime

from wtforms.fields.datetime import DateField
from wtforms.utils import clean_datetime_format_for_strptime, unset_value

from ..widgets import TnaDateInput


class TnaDateField(DateField):
    """
    A text field which stores a :class:`datetime.date` matching one or
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
                "%Y-%m-%d",
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
        self.invalid_parts = []
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
        self.invalid_parts = []
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

            if self.progressive and "" in raw_data:
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

    def process_data(self, value):
        if value:
            if type(value) is date:
                self.data = value
                return
            for format in self.strptime_format:
                try:
                    self.data = (
                        datetime.strptime(value, format).replace(tzinfo=UTC).date()
                    )
                    return
                except ValueError:
                    pass
        self.data = None

    def process_formdata(self, valuelist):
        self.invalid_parts = []
        if not valuelist:
            self.invalid_parts = self._get_invalid_parts(valuelist)
            return

        if self.progressive and "" in valuelist:
            valuelist = valuelist[: valuelist.index("")]

        date_str = " ".join([value for value in valuelist if value])
        for format in self.strptime_format:
            try:
                self.data = (
                    datetime.strptime(date_str, format).replace(tzinfo=UTC).date()
                )
                return
            except ValueError:
                self.data = None

        self.invalid_parts = self._get_invalid_parts(valuelist)
        raise ValueError(self.gettext(self.invalid_date_error_message))

    def _get_invalid_parts(self, valuelist):
        part_formats = {
            "day": {"%d"},
            "month": {"%m", "%b", "%B"},
            "year": {"%Y", "%y"},
        }
        formats = {
            directive
            for format in self.strptime_format
            for directive in format.replace("-", " ").split()
        }
        invalid_parts = []
        parsed_parts = {}
        for index, part in enumerate(self.field_codes(True)):
            if self.progressive and index > 0 and index >= len(valuelist):
                break
            value = valuelist[index] if index < len(valuelist) else ""
            for format in part_formats[part] & formats:
                try:
                    if part == "day":
                        parsed = datetime.strptime(f"{value} 2000", f"{format} %Y")
                    else:
                        parsed = datetime.strptime(value, format)
                except ValueError:
                    continue
                parsed_parts[part] = getattr(parsed, part)
                break
            else:
                invalid_parts.append(part)

        if all(part in parsed_parts for part in ("day", "month")):
            last_day = calendar.monthrange(
                parsed_parts.get("year", 2000), parsed_parts["month"]
            )[1]
            if parsed_parts["day"] > last_day:
                invalid_parts.append("day")
        return [part for part in self.field_codes(True) if part in invalid_parts]


class TnaPartialDateField(TnaDateField):
    def __init__(
        self,
        label=None,
        validators=None,
        allow_two_digit_year=False,
        invalid_date_error_message="",
        end_of_partial_date_range=False,
        **kwargs,
    ):
        super().__init__(
            label,
            validators,
            allow_two_digit_year,
            invalid_date_error_message,
            **kwargs,
        )
        self.end_of_partial_date_range = end_of_partial_date_range
        self.format = [
            format
            for format in [
                "%Y",
                ("%y") if allow_two_digit_year else None,
                "%Y-%m",
                "%Y %m",
                ("%y %m") if allow_two_digit_year else None,
                "%Y %b",
                ("%y %b") if allow_two_digit_year else None,
                "%Y %B",
                ("%y %B") if allow_two_digit_year else None,
                "%Y-%m-%d",
                "%Y %m %d",
                ("%y %m %d") if allow_two_digit_year else None,
                "%Y %b %d",
                ("%y %b %d") if allow_two_digit_year else None,
                "%Y %B %d",
                ("%y %B %d") if allow_two_digit_year else None,
            ]
            if format is not None
        ]
        self.strptime_format = clean_datetime_format_for_strptime(self.format)

    def process_formdata(self, valuelist):
        self.invalid_parts = []
        if not valuelist:
            self.invalid_parts = self._get_invalid_parts(valuelist)
            return

        submitted_values = valuelist
        if "" in valuelist:
            valuelist = valuelist[: valuelist.index("")]

        has_year = len(valuelist) >= 1
        has_month = len(valuelist) >= 2
        has_day = len(valuelist) >= 3

        date_str = " ".join([value for value in valuelist if value])

        for format in self.strptime_format:
            try:
                parsed_date = (
                    datetime.strptime(date_str, format).replace(tzinfo=UTC).date()
                )

                if self.end_of_partial_date_range and not has_day:
                    if has_month and has_year:
                        parsed_date = parsed_date.replace(
                            day=calendar.monthrange(
                                parsed_date.year, parsed_date.month
                            )[1],
                        )
                    elif has_year:
                        parsed_date = parsed_date.replace(
                            month=12,
                            day=calendar.monthrange(
                                parsed_date.year, parsed_date.month
                            )[1],
                        )

                self.data = parsed_date
                return
            except ValueError:
                self.data = None

        self.invalid_parts = self._get_invalid_parts(submitted_values)
        raise ValueError(self.gettext(self.invalid_date_error_message))


class TnaMonthField(TnaPartialDateField):
    def __init__(
        self,
        label=None,
        validators=None,
        allow_two_digit_year=False,
        invalid_date_error_message="",
        end_of_partial_date_range=False,
        **kwargs,
    ):
        super().__init__(
            label,
            validators,
            allow_two_digit_year,
            invalid_date_error_message,
            end_of_partial_date_range,
            **kwargs,
        )
        self.format = [
            format
            for format in [
                "%Y-%m",
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


class TnaYearField(TnaPartialDateField):
    def __init__(
        self,
        label=None,
        validators=None,
        allow_two_digit_year=False,
        invalid_date_error_message="",
        end_of_partial_date_range=False,
        **kwargs,
    ):
        super().__init__(
            label,
            validators,
            allow_two_digit_year,
            invalid_date_error_message,
            end_of_partial_date_range,
            **kwargs,
        )
        self.format = [
            format
            for format in ["%Y", ("%y") if allow_two_digit_year else None]
            if format is not None
        ]
        self.strptime_format = clean_datetime_format_for_strptime(self.format)


class TnaProgressiveDateField(TnaPartialDateField):
    def __init__(
        self,
        label=None,
        validators=None,
        allow_two_digit_year=False,
        invalid_date_error_message="",
        end_of_partial_date_range=False,
        **kwargs,
    ):
        super().__init__(
            label,
            validators,
            allow_two_digit_year,
            invalid_date_error_message,
            end_of_partial_date_range,
            **kwargs,
        )
        self.progressive = True

    # def process_formdata(self, valuelist):
    #     if not valuelist:
    #         return

    #     if "" in valuelist:
    #         valuelist = valuelist[: valuelist.index("")]

    #     has_year = len(valuelist) >= 1
    #     has_month = len(valuelist) >= 2
    #     has_day = len(valuelist) >= 3

    #     date_str = " ".join([value for value in valuelist if value])

    #     for format in self.strptime_format:
    #         try:
    #             parsed_date = datetime.strptime(date_str, format, tz=UTC).date()

    #             if self.end_of_partial_date_range:
    #                 if has_day and has_month and has_year:
    #                     parsed_date = parsed_date.replace(
    #                         hour=23,
    #                         minute=59,
    #                         second=59,
    #                     )
    #                 elif has_month and has_year:
    #                     parsed_date = parsed_date.replace(
    #                         day=calendar.monthrange(
    #                             parsed_date.year, parsed_date.month
    #                         )[1],
    #                         hour=23,
    #                         minute=59,
    #                         second=59,
    #                     )
    #                 elif has_year:
    #                     parsed_date = parsed_date.replace(
    #                         month=12,
    #                         day=calendar.monthrange(
    #                             parsed_date.year, parsed_date.month
    #                         )[1],
    #                         hour=23,
    #                         minute=59,
    #                         second=59,
    #                     )

    #             self.data = parsed_date
    #             return
    #         except ValueError:
    #             self.data = None

    #     raise ValueError(self.gettext(self.invalid_date_error_message))
