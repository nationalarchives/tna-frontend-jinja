import datetime
import unittest

from flask_wtf import FlaskForm
from tna_frontend_jinja.wtforms import (
    TnaDateField,
    TnaMonthField,
    TnaProgressiveDateField,
    TnaYearField,
)
from tna_frontend_jinja.wtforms.validators import FutureDate, PastDate
from werkzeug.datastructures import MultiDict
from wtforms import validators

from app import app


class DateInputForm(FlaskForm):
    class Meta:
        csrf = False

    date = TnaDateField(
        validators=[],
    )


class MonthInputForm(FlaskForm):
    class Meta:
        csrf = False

    date = TnaMonthField(
        validators=[],
    )


class MonthInputEndOfRangeForm(FlaskForm):
    class Meta:
        csrf = False

    date = TnaMonthField(validators=[], end_of_partial_date_range=True)


class YearInputForm(FlaskForm):
    class Meta:
        csrf = False

    date = TnaYearField(
        validators=[],
    )


class YearInputEndOfRangeForm(FlaskForm):
    class Meta:
        csrf = False

    date = TnaYearField(validators=[], end_of_partial_date_range=True)


class YearInputTwoDigitForm(FlaskForm):
    class Meta:
        csrf = False

    date = TnaYearField(
        validators=[],
        allow_two_digit_year=True,
    )


class ProgressiveDateForm(FlaskForm):
    class Meta:
        csrf = False

    date = TnaProgressiveDateField(
        validators=[],
    )


class TestDateInputField(unittest.TestCase):
    def setUp(self):
        self.error_message_required = "Enter a date"
        self.error_message_invalid = "Date must be a real date"

    def test_empty(self):
        with app.test_request_context():
            form = DateInputForm()
            form.date.validators = [
                validators.InputRequired(message=self.error_message_required)
            ]
            complete = form.validate()
            assert form.errors == {"date": [self.error_message_required]}
            assert complete is False

    def test_happy_formdata(self):
        with app.test_request_context():
            formdata = MultiDict(
                [
                    ("date-day", "01"),
                    ("date-month", "02"),
                    ("date-year", "2003"),
                ]
            )
            form = DateInputForm(formdata=formdata)
            form.date.validators = [
                validators.InputRequired(message=self.error_message_required)
            ]
            assert form.date.data == datetime.date(2003, 2, 1)
            complete = form.validate()
            assert form.errors == {}
            assert complete is True

    def test_happy_data_string(self):
        with app.test_request_context():
            data = {"date": "01 02 2003"}
            form = DateInputForm(formdata=None, data=data)
            form.date.validators = [
                validators.DataRequired(message=self.error_message_required)
            ]
            assert form.date.data == datetime.date(2003, 2, 1)
            complete = form.validate()
            assert form.errors == {}
            assert complete is True

    def test_happy_data_string_iso(self):
        with app.test_request_context():
            data = {"date": "2003-02-01"}
            form = DateInputForm(formdata=None, data=data)
            form.date.validators = [
                validators.DataRequired(message=self.error_message_required)
            ]
            assert form.date.data == datetime.date(2003, 2, 1)
            complete = form.validate()
            assert form.errors == {}
            assert complete is True

    def test_happy_data_datetime(self):
        with app.test_request_context():
            data = {"date": datetime.date(2003, 2, 1)}
            form = DateInputForm(formdata=None, data=data)
            form.date.validators = [
                validators.DataRequired(message=self.error_message_required)
            ]
            assert form.date.data == datetime.date(2003, 2, 1)
            complete = form.validate()
            assert form.errors == {}
            assert complete is True

    def test_unhappy_data_string(self):
        with app.test_request_context():
            data = {"date": "01 13 2003"}
            form = DateInputForm(formdata=None, data=data)
            form.date.validators = [
                validators.DataRequired(message=self.error_message_required)
            ]
            assert form.date.data is None
            complete = form.validate()
            assert form.errors == {"date": [self.error_message_required]}
            assert complete is False

    def test_unhappy_data_string_iso(self):
        with app.test_request_context():
            data = {"date": "2003-13-01"}
            form = DateInputForm(formdata=None, data=data)
            form.date.validators = [
                validators.DataRequired(message=self.error_message_required)
            ]
            assert form.date.data is None
            complete = form.validate()
            assert form.errors == {"date": [self.error_message_required]}
            assert complete is False

    def test_happy_formdata_month_string(self):
        with app.test_request_context():
            formdata = MultiDict(
                [
                    ("date-day", "01"),
                    ("date-month", "feb"),
                    ("date-year", "2003"),
                ]
            )
            form = DateInputForm(formdata=formdata)
            form.date.validators = [
                validators.InputRequired(message=self.error_message_required)
            ]
            assert form.date.data == datetime.date(2003, 2, 1)
            complete = form.validate()
            assert form.errors == {}
            assert complete is True

    def test_unhappy_formdata_month_string(self):
        with app.test_request_context():
            formdata = MultiDict(
                [
                    ("date-day", "01"),
                    ("date-month", "xyz"),
                    ("date-year", "2003"),
                ]
            )
            form = DateInputForm(formdata=formdata)
            form.date.validators = [
                validators.InputRequired(message=self.error_message_required)
            ]
            assert form.date.data is None
            complete = form.validate()
            assert form.errors == {"date": [self.error_message_invalid]}
            assert complete is False

    def test_happy_data_month_string(self):
        with app.test_request_context():
            data = {"date": "01 feb 2003"}
            form = DateInputForm(formdata=None, data=data)
            form.date.validators = [
                validators.DataRequired(message=self.error_message_required)
            ]
            assert form.date.data == datetime.date(2003, 2, 1)
            complete = form.validate()
            assert form.errors == {}
            assert complete is True

    def test_unhappy_data_month_string(self):
        with app.test_request_context():
            data = {"date": "01 xyz 2003"}
            form = DateInputForm(formdata=None, data=data)
            form.date.validators = [
                validators.DataRequired(message=self.error_message_required)
            ]
            assert form.date.data is None
            complete = form.validate()
            assert form.errors == {"date": [self.error_message_required]}
            assert complete is False

    def test_partial_formdata(self):
        with app.test_request_context():
            formdata = MultiDict(
                [("date-day", ""), ("date-month", "02"), ("date-year", "2003")]
            )
            form = DateInputForm(formdata=formdata)
            form.date.validators = [
                validators.InputRequired(message=self.error_message_required)
            ]
            assert form.date.data is None
            complete = form.validate()
            assert form.errors == {"date": [self.error_message_required]}
            assert complete is False

    def test_partial_data(self):
        with app.test_request_context():
            data = {"date": "02 2003"}
            form = DateInputForm(formdata=None, data=data)
            form.date.validators = [
                validators.DataRequired(message=self.error_message_required)
            ]
            assert form.date.data is None
            complete = form.validate()
            assert form.errors == {"date": [self.error_message_required]}
            assert complete is False


class TestMonthInputField(unittest.TestCase):
    def setUp(self):
        self.error_message_required = "Enter a date"
        self.error_message_invalid = "Date must be a real date"

    def test_happy_formdata(self):
        with app.test_request_context():
            formdata = MultiDict([("date-month", "02"), ("date-year", "2003")])
            form = MonthInputForm(formdata=formdata)
            form.date.validators = [
                validators.InputRequired(message=self.error_message_required)
            ]
            assert form.date.data == datetime.date(2003, 2, 1)
            complete = form.validate()
            assert form.errors == {}
            assert complete is True

    def test_happy_data(self):
        with app.test_request_context():
            data = {"date": "02 2003"}
            form = MonthInputForm(formdata=None, data=data)
            form.date.validators = [
                validators.DataRequired(message=self.error_message_required)
            ]
            assert form.date.data == datetime.date(2003, 2, 1)
            complete = form.validate()
            assert form.errors == {}
            assert complete is True

    def test_happy_data_string_iso(self):
        with app.test_request_context():
            data = {"date": "2003-02"}
            form = MonthInputForm(formdata=None, data=data)
            form.date.validators = [
                validators.DataRequired(message=self.error_message_required)
            ]
            assert form.date.data == datetime.date(2003, 2, 1)
            complete = form.validate()
            assert form.errors == {}
            assert complete is True

    def test_happy_data_datetime(self):
        with app.test_request_context():
            data = {"date": datetime.date(2003, 2, 1)}
            form = MonthInputForm(formdata=None, data=data)
            form.date.validators = [
                validators.DataRequired(message=self.error_message_required)
            ]
            assert form.date.data == datetime.date(2003, 2, 1)
            complete = form.validate()
            assert form.errors == {}
            assert complete is True

    def test_unhappy_formdata(self):
        with app.test_request_context():
            formdata = MultiDict([("date-month", "13"), ("date-year", "2003")])
            form = MonthInputForm(formdata=formdata)
            form.date.validators = [
                validators.InputRequired(message=self.error_message_required)
            ]
            assert form.date.data is None
            complete = form.validate()
            assert form.errors == {"date": [self.error_message_invalid]}
            assert complete is False

    def test_unhappy_data(self):
        with app.test_request_context():
            data = {"date": "13 2003"}
            form = MonthInputForm(formdata=None, data=data)
            form.date.validators = [
                validators.DataRequired(message=self.error_message_required)
            ]
            assert form.date.data is None
            complete = form.validate()
            assert form.errors == {"date": [self.error_message_required]}
            assert complete is False

    def test_unhappy_data_string_iso(self):
        with app.test_request_context():
            data = {"date": "2003-13"}
            form = MonthInputForm(formdata=None, data=data)
            form.date.validators = [
                validators.DataRequired(message=self.error_message_required)
            ]
            assert form.date.data is None
            complete = form.validate()
            assert form.errors == {"date": [self.error_message_required]}
            assert complete is False

    def test_happy_formdata_month_string(self):
        with app.test_request_context():
            formdata = MultiDict([("date-month", "feb"), ("date-year", "2003")])
            form = MonthInputForm(formdata=formdata)
            form.date.validators = [
                validators.InputRequired(message=self.error_message_required)
            ]
            assert form.date.data == datetime.date(2003, 2, 1)
            complete = form.validate()
            assert form.errors == {}
            assert complete is True

    def test_unhappy_formdata_month_string(self):
        with app.test_request_context():
            formdata = MultiDict([("date-month", "xyz"), ("date-year", "2003")])
            form = MonthInputForm(formdata=formdata)
            form.date.validators = [
                validators.InputRequired(message=self.error_message_required)
            ]
            assert form.date.data is None
            complete = form.validate()
            assert form.errors == {"date": [self.error_message_invalid]}
            assert complete is False

    def test_end_of_range(self):
        with app.test_request_context():
            formdata = MultiDict([("date-month", "02"), ("date-year", "2003")])
            form = MonthInputEndOfRangeForm(formdata=formdata)
            form.date.validators = [
                validators.InputRequired(message=self.error_message_required)
            ]
            assert form.date.data == datetime.date(2003, 2, 28)
            complete = form.validate()
            assert form.errors == {}
            assert complete is True

    def test_partial_formdata(self):
        with app.test_request_context():
            formdata = MultiDict([("date-month", ""), ("date-year", "2003")])
            form = MonthInputForm(formdata=formdata)
            form.date.validators = [
                validators.InputRequired(message=self.error_message_required)
            ]
            assert form.date.data is None
            complete = form.validate()
            assert form.errors == {"date": [self.error_message_required]}
            assert complete is False

    def test_partial_data(self):
        with app.test_request_context():
            data = {"date": "2003"}
            form = MonthInputForm(formdata=None, data=data)
            form.date.validators = [
                validators.DataRequired(message=self.error_message_required)
            ]
            assert form.date.data is None
            complete = form.validate()
            assert form.errors == {"date": [self.error_message_required]}
            assert complete is False


class TestYearInputField(unittest.TestCase):
    def setUp(self):
        self.error_message_required = "Enter a date"
        self.error_message_invalid = "Date must be a real date"

    def test_happy_formdata(self):
        with app.test_request_context():
            formdata = MultiDict([("date-year", "2003")])
            form = YearInputForm(formdata=formdata)
            form.date.validators = [
                validators.InputRequired(message=self.error_message_required)
            ]
            assert form.date.data == datetime.date(2003, 1, 1)
            complete = form.validate()
            assert form.errors == {}
            assert complete is True

    def test_happy_data_string(self):
        with app.test_request_context():
            data = {"date": "2003"}
            form = YearInputForm(formdata=None, data=data)
            form.date.validators = [
                validators.DataRequired(message=self.error_message_required)
            ]
            assert form.date.data == datetime.date(2003, 1, 1)
            complete = form.validate()
            assert form.errors == {}
            assert complete is True

    def test_happy_data_datetime(self):
        with app.test_request_context():
            data = {"date": datetime.date(2003, 1, 1)}
            form = YearInputForm(formdata=None, data=data)
            form.date.validators = [
                validators.DataRequired(message=self.error_message_required)
            ]
            assert form.date.data == datetime.date(2003, 1, 1)
            complete = form.validate()
            assert form.errors == {}
            assert complete is True

    def test_unhappy_formdata(self):
        with app.test_request_context():
            formdata = MultiDict([("date-year", "xyz")])
            form = YearInputForm(formdata=formdata)
            form.date.validators = [
                validators.InputRequired(message=self.error_message_required)
            ]
            assert form.date.data is None
            complete = form.validate()
            assert form.errors == {"date": [self.error_message_invalid]}
            assert complete is False

    def test_end_of_range(self):
        with app.test_request_context():
            formdata = MultiDict([("date-year", "2003")])
            form = YearInputEndOfRangeForm(formdata=formdata)
            form.date.validators = [
                validators.InputRequired(message=self.error_message_required)
            ]
            assert form.date.data == datetime.date(2003, 12, 31)
            complete = form.validate()
            assert form.errors == {}
            assert complete is True

    def test_two_digit(self):
        with app.test_request_context():
            formdata = MultiDict([("date-year", "2003")])
            form = YearInputTwoDigitForm(formdata=formdata)
            assert form.date.data == datetime.date(2003, 1, 1)

            formdata = MultiDict([("date-year", "03")])
            form = YearInputTwoDigitForm(formdata=formdata)
            assert form.date.data == datetime.date(2003, 1, 1)

            formdata = MultiDict([("date-year", "99")])
            form = YearInputTwoDigitForm(formdata=formdata)
            assert form.date.data == datetime.date(1999, 1, 1)

            formdata = MultiDict([("date-year", "00")])
            form = YearInputTwoDigitForm(formdata=formdata)
            assert form.date.data == datetime.date(2000, 1, 1)


class TestProgressiveDateInputField(unittest.TestCase):
    def setUp(self):
        self.error_message_required = "Enter a date"
        self.error_message_invalid = "Date must be a real date"

    def test_happy_formdata_year(self):
        with app.test_request_context():
            formdata = MultiDict([("date-year", "2004")])
            form = ProgressiveDateForm(formdata=formdata)
            form.date.validators = [
                validators.InputRequired(message=self.error_message_required)
            ]
            assert form.date.data == datetime.date(2004, 1, 1)
            complete = form.validate()
            assert form.errors == {}
            assert complete is True

    def test_happy_formdata_year_month(self):
        with app.test_request_context():
            formdata = MultiDict([("date-month", "03"), ("date-year", "2004")])
            form = ProgressiveDateForm(formdata=formdata)
            form.date.validators = [
                validators.InputRequired(message=self.error_message_required)
            ]
            assert form.date.data == datetime.date(2004, 3, 1)
            complete = form.validate()
            assert form.errors == {}
            assert complete is True

    def test_happy_formdata_year_month_day(self):
        with app.test_request_context():
            formdata = MultiDict(
                [
                    ("date-day", "02"),
                    ("date-month", "03"),
                    ("date-year", "2004"),
                ]
            )
            form = ProgressiveDateForm(formdata=formdata)
            form.date.validators = [
                validators.InputRequired(message=self.error_message_required)
            ]
            assert form.date.data == datetime.date(2004, 3, 2)
            complete = form.validate()
            assert form.errors == {}
            assert complete is True

    def test_happy_data_string_year(self):
        with app.test_request_context():
            data = {"date": "2004"}
            form = ProgressiveDateForm(formdata=None, data=data)
            form.date.validators = [
                validators.DataRequired(message=self.error_message_required)
            ]
            assert form.date.data == datetime.date(2004, 1, 1)
            complete = form.validate()
            assert form.errors == {}
            assert complete is True

    def test_happy_data_string_year_month(self):
        with app.test_request_context():
            data = {"date": "2004 03"}
            form = ProgressiveDateForm(formdata=None, data=data)
            form.date.validators = [
                validators.DataRequired(message=self.error_message_required)
            ]
            assert form.date.data == datetime.date(2004, 3, 1)
            complete = form.validate()
            assert form.errors == {}
            assert complete is True

    def test_happy_data_string_year_month_iso(self):
        with app.test_request_context():
            data = {"date": "2004-03"}
            form = ProgressiveDateForm(formdata=None, data=data)
            form.date.validators = [
                validators.DataRequired(message=self.error_message_required)
            ]
            assert form.date.data == datetime.date(2004, 3, 1)
            complete = form.validate()
            assert form.errors == {}
            assert complete is True

    def test_happy_data_string_year_month_day(self):
        with app.test_request_context():
            data = {"date": "2004 03 02"}
            form = ProgressiveDateForm(formdata=None, data=data)
            form.date.validators = [
                validators.DataRequired(message=self.error_message_required)
            ]
            assert form.date.data == datetime.date(2004, 3, 2)
            complete = form.validate()
            assert form.errors == {}
            assert complete is True

    def test_happy_data_string_year_month_day_iso(self):
        with app.test_request_context():
            data = {"date": "2004-03-02"}
            form = ProgressiveDateForm(formdata=None, data=data)
            form.date.validators = [
                validators.DataRequired(message=self.error_message_required)
            ]
            assert form.date.data == datetime.date(2004, 3, 2)
            complete = form.validate()
            assert form.errors == {}
            assert complete is True

        # TODO: end_of_partial_date_range


class TestPastDateValidator(unittest.TestCase):
    def setUp(self):
        self.error_message_past_date = "The date must be in the past"

    def test_happy_formdata(self):
        with app.test_request_context():
            formdata = MultiDict(
                [
                    ("date-day", "01"),
                    ("date-month", "02"),
                    ("date-year", "2003"),
                ]
            )
            form = DateInputForm(formdata=formdata)
            form.date.validators = [PastDate()]
            assert form.date.data == datetime.date(2003, 2, 1)
            complete = form.validate()
            assert form.errors == {}
            assert complete is True

    def test_happy_data_string(self):
        with app.test_request_context():
            data = {"date": "01 02 2003"}
            form = DateInputForm(formdata=None, data=data)
            form.date.validators = [PastDate()]
            assert form.date.data == datetime.date(2003, 2, 1)
            complete = form.validate()
            assert form.errors == {}
            assert complete is True

    def test_happy_data_string_iso(self):
        with app.test_request_context():
            data = {"date": "2003-02-01"}
            form = DateInputForm(formdata=None, data=data)
            form.date.validators = [PastDate()]
            assert form.date.data == datetime.date(2003, 2, 1)
            complete = form.validate()
            assert form.errors == {}
            assert complete is True

    def test_happy_data_datetime(self):
        with app.test_request_context():
            data = {"date": datetime.date(2003, 2, 1)}
            form = DateInputForm(formdata=None, data=data)
            form.date.validators = [PastDate()]
            assert form.date.data == datetime.date(2003, 2, 1)
            complete = form.validate()
            assert form.errors == {}
            assert complete is True

    def test_unhappy_formdata(self):
        with app.test_request_context():
            formdata = MultiDict(
                [
                    ("date-day", "01"),
                    ("date-month", "02"),
                    ("date-year", "2103"),
                ]
            )
            form = DateInputForm(formdata=formdata)
            form.date.validators = [
                PastDate(message=self.error_message_past_date)
            ]
            assert form.date.data == datetime.date(2103, 2, 1)
            complete = form.validate()
            assert form.errors == {"date": [self.error_message_past_date]}
            assert complete is False

    def test_unhappy_data_string(self):
        with app.test_request_context():
            data = {"date": "01 02 2103"}
            form = DateInputForm(formdata=None, data=data)
            form.date.validators = [
                PastDate(message=self.error_message_past_date)
            ]
            assert form.date.data == datetime.date(2103, 2, 1)
            complete = form.validate()
            assert form.errors == {"date": [self.error_message_past_date]}
            assert complete is False

    def test_unhappy_data_string_iso(self):
        with app.test_request_context():
            data = {"date": "2103-02-01"}
            form = DateInputForm(formdata=None, data=data)
            form.date.validators = [
                PastDate(message=self.error_message_past_date)
            ]
            assert form.date.data == datetime.date(2103, 2, 1)
            complete = form.validate()
            assert form.errors == {"date": [self.error_message_past_date]}
            assert complete is False

    def test_unhappy_data_datetime(self):
        with app.test_request_context():
            data = {"date": datetime.date(2103, 2, 1)}
            form = DateInputForm(formdata=None, data=data)
            form.date.validators = [
                PastDate(message=self.error_message_past_date)
            ]
            assert form.date.data == datetime.date(2103, 2, 1)
            complete = form.validate()
            assert form.errors == {"date": [self.error_message_past_date]}
            assert complete is False


class TestFutureDateValidator(unittest.TestCase):
    def setUp(self):
        self.error_message_future_date = "The date must be in the future"

    def test_happy_formdata(self):
        with app.test_request_context():
            formdata = MultiDict(
                [
                    ("date-day", "01"),
                    ("date-month", "02"),
                    ("date-year", "2103"),
                ]
            )
            form = DateInputForm(formdata=formdata)
            form.date.validators = [FutureDate()]
            assert form.date.data == datetime.date(2103, 2, 1)
            complete = form.validate()
            assert form.errors == {}
            assert complete is True

    def test_happy_data_string(self):
        with app.test_request_context():
            data = {"date": "01 02 2103"}
            form = DateInputForm(formdata=None, data=data)
            form.date.validators = [FutureDate()]
            assert form.date.data == datetime.date(2103, 2, 1)
            complete = form.validate()
            assert form.errors == {}
            assert complete is True

    def test_happy_data_string_iso(self):
        with app.test_request_context():
            data = {"date": "2103-02-01"}
            form = DateInputForm(formdata=None, data=data)
            form.date.validators = [FutureDate()]
            assert form.date.data == datetime.date(2103, 2, 1)
            complete = form.validate()
            assert form.errors == {}
            assert complete is True

    def test_happy_data_datetime(self):
        with app.test_request_context():
            data = {"date": datetime.date(2103, 2, 1)}
            form = DateInputForm(formdata=None, data=data)
            form.date.validators = [FutureDate()]
            assert form.date.data == datetime.date(2103, 2, 1)
            complete = form.validate()
            assert form.errors == {}
            assert complete is True

    def test_unhappy_formdata(self):
        with app.test_request_context():
            formdata = MultiDict(
                [
                    ("date-day", "01"),
                    ("date-month", "02"),
                    ("date-year", "2003"),
                ]
            )
            form = DateInputForm(formdata=formdata)
            form.date.validators = [
                FutureDate(message=self.error_message_future_date)
            ]
            assert form.date.data == datetime.date(2003, 2, 1)
            complete = form.validate()
            assert form.errors == {"date": [self.error_message_future_date]}
            assert complete is False

    def test_unhappy_data_string(self):
        with app.test_request_context():
            data = {"date": "01 02 2003"}
            form = DateInputForm(formdata=None, data=data)
            form.date.validators = [
                FutureDate(message=self.error_message_future_date)
            ]
            assert form.date.data == datetime.date(2003, 2, 1)
            complete = form.validate()
            assert form.errors == {"date": [self.error_message_future_date]}
            assert complete is False

    def test_unhappy_data_string_iso(self):
        with app.test_request_context():
            data = {"date": "2003-02-01"}
            form = DateInputForm(formdata=None, data=data)
            form.date.validators = [
                FutureDate(message=self.error_message_future_date)
            ]
            assert form.date.data == datetime.date(2003, 2, 1)
            complete = form.validate()
            assert form.errors == {"date": [self.error_message_future_date]}
            assert complete is False

    def test_unhappy_data_datetime(self):
        with app.test_request_context():
            data = {"date": datetime.date(2003, 2, 1)}
            form = DateInputForm(formdata=None, data=data)
            form.date.validators = [
                FutureDate(message=self.error_message_future_date)
            ]
            assert form.date.data == datetime.date(2003, 2, 1)
            complete = form.validate()
            assert form.errors == {"date": [self.error_message_future_date]}
            assert complete is False
