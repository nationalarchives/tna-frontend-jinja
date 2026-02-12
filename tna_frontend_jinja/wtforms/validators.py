import datetime
import re

from wtforms import ValidationError


class FutureDate:
    """
    Validates a date is in the future.

    :param message:
        Error message to raise in case of a validation error.
    """

    def __init__(self, message=None, include_now=False):
        self.message = message
        self.include_now = include_now

    def __call__(self, form, field):
        message = self.message
        if message is None:
            message = field.gettext("Date must be in the future")
        try:
            if not field.data:
                raise ValidationError(message)
            try:
                field_date = field.data.date()
            except AttributeError:
                field_date = field.data
            if type(field_date) is not datetime.date:
                try:
                    field_date = datetime.date.fromisoformat(field.data)
                except Exception:
                    raise ValueError()
            if (self.include_now and field_date < datetime.date.today()) or (
                not self.include_now and field_date <= datetime.date.today()
            ):
                raise ValueError(message)
        except ValueError as exc:
            raise ValidationError(message) from exc


class PastDate:
    """
    Validates a date is in the past.

    :param message:
        Error message to raise in case of a validation error.
    """

    def __init__(self, message=None, include_now=False):
        self.message = message
        self.include_now = include_now

    def __call__(self, form, field):
        message = self.message
        if message is None:
            message = field.gettext("Date must be in the past")
        try:
            if not field.data:
                raise ValidationError(message)
            try:
                field_date = field.data.date()
            except AttributeError:
                field_date = field.data
            if type(field_date) is not datetime.date:
                try:
                    field_date = datetime.date.fromisoformat(field.data)
                except Exception:
                    raise ValueError()
            if (self.include_now and field_date > datetime.date.today()) or (
                not self.include_now and field_date >= datetime.date.today()
            ):
                raise ValueError(message)
        except ValueError as exc:
            raise ValidationError(message) from exc


class MaxOptions:
    """
    Validates a list of values doesn't exceed a given maximum.

    :param message:
        Error message to raise in case of a validation error.
    """

    def __init__(self, max=-1, message=None):
        assert max != -1, "`max` must be specified."
        self.max = max
        self.message = message

    def __call__(self, form, field):
        message = self.message
        if message is None:
            message = field.gettext(
                f"You must select no more than {self.max} options"
            )
        try:
            if len(field.data) > self.max:
                raise ValidationError(message)
        except ValueError as exc:
            raise ValidationError(message) from exc


class UKPostcode:
    """
    Validates a postcode in the UK format.

    :param message:
        Error message to raise in case of a validation error.
    """

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        message = self.message
        if message is None:
            message = field.gettext("Enter a valid UK postcode")
        try:
            if not field.data:
                raise ValidationError(message)
            postcode = field.data.strip().replace(" ", "")
            if not re.match(
                r"^([Gg][Ii][Rr] 0[Aa]{2})|((([A-Za-z][0-9]{1,2})|(([A-Za-z][A-Ha-hJ-Yj-y][0-9]{1,2})|(([A-Za-z][0-9][A-Za-z])|([A-Za-z][A-Ha-hJ-Yj-y][0-9]?[A-Za-z])))) ?[0-9][A-Za-z]{2})$",
                postcode,
            ):
                raise ValueError(message)
        except ValueError as exc:
            raise ValidationError(message) from exc
