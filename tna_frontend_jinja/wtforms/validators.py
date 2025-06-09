import datetime

from wtforms import ValidationError


class FutureDate:
    """
    Validates a date is in the future.

    :param message:
        Error message to raise in case of a validation error.
    """

    def __init__(self, message=None, include_today=False):
        self.message = message
        self.include_today = include_today

    def __call__(self, form, field):
        message = self.message
        if message is None:
            message = field.gettext("Date must be in the future")
        try:
            if (self.include_today and field.data < datetime.date.today()) or (
                not self.include_today and field.data <= datetime.date.today()
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

    def __init__(self, message=None, include_today=False):
        self.message = message
        self.include_today = include_today

    def __call__(self, form, field):
        message = self.message
        if message is None:
            message = field.gettext("Date must be in the past")
        try:
            if (self.include_today and field.data > datetime.date.today()) or (
                not self.include_today and field.data >= datetime.date.today()
            ):
                raise ValueError(message)
        except ValueError as exc:
            raise ValidationError(message) from exc
