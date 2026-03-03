import datetime
import unittest

from flask_wtf import FlaskForm
from tna_frontend_jinja.wtforms import (
    TnaDateField,
)
from tna_frontend_jinja.wtforms.validators import (
    FutureDate,
    MaxOptions,
    PastDate,
    UKPostcode,
)
from werkzeug.datastructures import MultiDict
from wtforms import RadioField, StringField

from app import app


class TextInputForm(FlaskForm):
    class Meta:
        csrf = False

    string = StringField(
        validators=[],
    )


class DateInputForm(FlaskForm):
    class Meta:
        csrf = False

    date = TnaDateField(
        validators=[],
    )


class RadioForm(FlaskForm):
    class Meta:
        csrf = False

    string = RadioField(
        "Day",
        choices=[
            ("1", "Monday"),
            ("2", "Tuesday"),
            ("3", "Wednesday"),
            ("4", "Thursday"),
            ("5", "Friday"),
        ],
        validators=[],
    )


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


class TestMaxOptionsValidator(unittest.TestCase):
    def test_happy_formdata(self):
        with app.test_request_context():
            formdata = MultiDict(
                [
                    ("string", "1"),
                ]
            )
            form = RadioForm(formdata=formdata)
            form.string.validators = [MaxOptions(5)]
            assert form.string.data == "1"
            complete = form.validate()
            assert form.errors == {}
            assert complete is True

    def test_unhappy_formdata(self):
        with app.test_request_context():
            formdata = MultiDict(
                [
                    ("string", "1"),
                ]
            )
            form = RadioForm(formdata=formdata)
            form.string.validators = [MaxOptions(0, message="Too many options")]
            assert form.string.data == "1"
            complete = form.validate()
            assert form.errors == {"string": ["Too many options"]}
            assert complete is False


class TestUKPostcodeValidator(unittest.TestCase):
    def test_happy_formdata(self):
        with app.test_request_context():
            formdata = MultiDict(
                [
                    ("string", "SW1A 1AA"),
                ]
            )
            form = TextInputForm(formdata=formdata)
            form.string.validators = [UKPostcode()]
            assert form.string.data == "SW1A 1AA"
            complete = form.validate()
            assert form.errors == {}
            assert complete is True

    def test_unhappy_formdata(self):
        with app.test_request_context():
            formdata = MultiDict(
                [
                    ("string", "INVALID"),
                ]
            )
            form = TextInputForm(formdata=formdata)
            form.string.validators = [
                UKPostcode(message="Enter a valid postcode")
            ]
            assert form.string.data == "INVALID"
            complete = form.validate()
            assert form.errors == {"string": ["Enter a valid postcode"]}
            assert complete is False
