import datetime
import unittest

from flask_wtf import FlaskForm
from tna_frontend_jinja.wtforms import TnaDateField
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


class TestDateInput(unittest.TestCase):
    def setUp(self):
        self.error_message_required = "Enter a date"
        self.error_message_invalid = "Date must be a real date"

    def test_empty_form(self):
        with app.test_request_context():
            form = DateInputForm()
            form.date.validators = [
                validators.InputRequired(message=self.error_message_required)
            ]
            complete = form.validate()
            assert form.errors == {"date": [self.error_message_required]}
            assert complete is False

    def test_with_data(self):
        with app.test_request_context():
            formdata = MultiDict(
                [("date-day", "01"), ("date-month", "02"), ("date-year", "2003")]
            )
            form = DateInputForm(formdata=formdata)
            form.date.validators = [
                validators.InputRequired(message=self.error_message_required)
            ]
            assert form.date.data == datetime.date(2003, 2, 1)
            complete = form.validate()
            assert form.errors == {}
            assert complete is True

            data = {"date": "01 02 2003"}
            form = DateInputForm(formdata=None, data=data)
            form.date.validators = [
                validators.DataRequired(message=self.error_message_required)
            ]
            assert form.date.data == datetime.date(2003, 2, 1)
            complete = form.validate()
            assert form.errors == {}
            assert complete is True

    def test_with_month_string(self):
        with app.test_request_context():
            formdata = MultiDict(
                [("date-day", "01"), ("date-month", "feb"), ("date-year", "2003")]
            )
            form = DateInputForm(formdata=formdata)
            form.date.validators = [
                validators.InputRequired(message=self.error_message_required)
            ]
            assert form.date.data == datetime.date(2003, 2, 1)
            complete = form.validate()
            assert form.errors == {}
            assert complete is True

    def test_with_invalid_month_string(self):
        with app.test_request_context():
            formdata = MultiDict(
                [("date-day", "01"), ("date-month", "xyz"), ("date-year", "2003")]
            )
            form = DateInputForm(formdata=formdata)
            form.date.validators = [
                validators.InputRequired(message=self.error_message_required)
            ]
            assert form.date.data is None
            complete = form.validate()
            assert form.errors == {"date": [self.error_message_invalid]}
            assert complete is False

    def test_with_partial_data(self):
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

    def test_with_invalid_data(self):
        with app.test_request_context():
            formdata = MultiDict(
                [("date-day", "01"), ("date-month", "13"), ("date-year", "2003")]
            )
            form = DateInputForm(formdata=formdata)
            form.date.validators = [
                validators.InputRequired(message=self.error_message_required)
            ]
            assert form.date.data is None
            complete = form.validate()
            assert form.errors == {"date": [self.error_message_invalid]}
            assert complete is False

    def test_PastDate_validator_pass(self):
        with app.test_request_context():
            formdata = MultiDict(
                [("date-day", "01"), ("date-month", "02"), ("date-year", "2003")]
            )
            form = DateInputForm(formdata=formdata)
            form.date.validators = [PastDate()]
            assert form.date.data == datetime.date(2003, 2, 1)
            complete = form.validate()
            assert form.errors == {}
            assert complete is True

            data = {"date": "01 02 2003"}
            form = DateInputForm(formdata=None, data=data)
            form.date.validators = [PastDate()]
            assert form.date.data == datetime.date(2003, 2, 1)
            complete = form.validate()
            assert form.errors == {}
            assert complete is True

    def test_PastDate_validator_fail(self):
        error_message_past_date = "The date must be in the past"
        with app.test_request_context():
            formdata = MultiDict(
                [("date-day", "01"), ("date-month", "02"), ("date-year", "2103")]
            )
            form = DateInputForm(formdata=formdata)
            form.date.validators = [PastDate(message=error_message_past_date)]
            assert form.date.data == datetime.date(2103, 2, 1)
            complete = form.validate()
            assert form.errors == {"date": [error_message_past_date]}
            assert complete is False

            data = {"date": "01 02 2103"}
            form = DateInputForm(formdata=None, data=data)
            form.date.validators = [PastDate(message=error_message_past_date)]
            assert form.date.data == datetime.date(2103, 2, 1)
            complete = form.validate()
            assert form.errors == {"date": [error_message_past_date]}
            assert complete is False

    def test_FutureDate_validator_pass(self):
        with app.test_request_context():
            formdata = MultiDict(
                [("date-day", "01"), ("date-month", "02"), ("date-year", "2103")]
            )
            form = DateInputForm(formdata=formdata)
            form.date.validators = [FutureDate()]
            assert form.date.data == datetime.date(2103, 2, 1)
            complete = form.validate()
            assert form.errors == {}
            assert complete is True

            data = {"date": "01 02 2103"}
            form = DateInputForm(formdata=None, data=data)
            form.date.validators = [FutureDate()]
            assert form.date.data == datetime.date(2103, 2, 1)
            complete = form.validate()
            assert form.errors == {}
            assert complete is True

    def test_FutureDate_validator_fail(self):
        error_message_past_date = "The date must be in the past"
        with app.test_request_context():
            formdata = MultiDict(
                [("date-day", "01"), ("date-month", "02"), ("date-year", "2003")]
            )
            form = DateInputForm(formdata=formdata)
            form.date.validators = [FutureDate(message=error_message_past_date)]
            assert form.date.data == datetime.date(2003, 2, 1)
            complete = form.validate()
            assert form.errors == {"date": [error_message_past_date]}
            assert complete is False

            data = {"date": "01 02 2003"}
            form = DateInputForm(formdata=None, data=data)
            form.date.validators = [FutureDate(message=error_message_past_date)]
            assert form.date.data == datetime.date(2003, 2, 1)
            complete = form.validate()
            assert form.errors == {"date": [error_message_past_date]}
            assert complete is False
