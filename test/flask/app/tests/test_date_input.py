import datetime
import unittest

from flask_wtf import FlaskForm
from werkzeug.datastructures import MultiDict
from wtforms import validators

from app import app
from tna_frontend_jinja.wtforms import (
    TnaDateField,
    TnaMonthField,
    TnaProgressiveDateField,
    TnaYearField,
)


class DateInputForm(FlaskForm):
    class Meta:
        csrf = False

    date = TnaDateField(
        validators=[],
    )


class CustomInvalidDateMessageForm(FlaskForm):
    class Meta:
        csrf = False

    date = TnaDateField(
        "Date",
        validators=[],
        invalid_value_message="Enter a valid calendar date",
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
        self.error_message_invalid = "Enter a real date"

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

    def test_invalid_value_message(self):
        with app.test_request_context():
            formdata = MultiDict(
                [
                    ("date-day", "01"),
                    ("date-month", "13"),
                    ("date-year", "2003"),
                ]
            )
            form = CustomInvalidDateMessageForm(formdata=formdata)
            assert form.date.data is None
            assert form.validate() is False
            assert form.errors == {"date": ["Enter a valid calendar date"]}

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


class TestInvalidDateParts(unittest.TestCase):
    def test_full_date_invalid_parts(self):
        cases = [
            (["01", "02", "2003"], []),
            (["01", "February", "2003"], []),
            (["", "02", "2003"], ["day"]),
            (["01", "", "2003"], ["month"]),
            (["01", "02", ""], ["year"]),
            (["", "", ""], ["day", "month", "year"]),
            (["abc", "02", "2003"], ["day"]),
            (["00", "02", "2003"], ["day"]),
            (["32", "02", "2003"], ["day"]),
            (["01", "xyz", "2003"], ["month"]),
            (["01", "00", "2003"], ["month"]),
            (["01", "13", "2003"], ["month"]),
            (["01", "02", "abc"], ["year"]),
            (["01", "02", "0000"], ["year"]),
            (["01", "02", "10000"], ["year"]),
            (["01", "02", "03"], ["year"]),
            (["31", "04", "2003"], ["day"]),
            (["29", "feb", "2003"], ["day"]),
            (["29", "feb", "2004"], []),
            (["29", "02", "1900"], ["day"]),
            (["29", "02", "2000"], []),
            (["30", "02", "abc"], ["day", "year"]),
            (["31", "04", ""], ["day", "year"]),
            (["29", "02", "abc"], ["year"]),
            (["32", "13", "abc"], ["day", "month", "year"]),
        ]
        with app.test_request_context():
            for values, expected in cases:
                with self.subTest(values=values):
                    formdata = MultiDict(
                        zip(
                            ["date-day", "date-month", "date-year"],
                            values,
                            strict=False,
                        )
                    )
                    form = DateInputForm(formdata=formdata)
                    assert form.date.invalid_parts == expected
                    assert form.validate() is (not expected)
                    assert form.errors == (
                        {"date": ["Enter a real date"]} if expected else {}
                    )

    def test_partial_date_invalid_parts(self):
        cases = [
            (MonthInputForm, ["02", "2003"], []),
            (MonthInputForm, ["xyz", "2003"], ["month"]),
            (MonthInputForm, ["02", "abc"], ["year"]),
            (MonthInputForm, ["", "2003"], ["month"]),
            (MonthInputForm, ["02", ""], ["year"]),
            (MonthInputForm, ["", ""], ["month", "year"]),
            (YearInputForm, ["2003"], []),
            (YearInputForm, ["abc"], ["year"]),
            (YearInputForm, [""], ["year"]),
            (YearInputTwoDigitForm, ["03"], []),
            (ProgressiveDateForm, ["2003", "", ""], []),
            (ProgressiveDateForm, ["2003", "02", ""], []),
            (ProgressiveDateForm, ["2003", "13", ""], ["month"]),
            (ProgressiveDateForm, ["abc", "", ""], ["year"]),
            (ProgressiveDateForm, ["", "", ""], ["year"]),
            (ProgressiveDateForm, ["2003", "04", "31"], ["day"]),
            (ProgressiveDateForm, ["2003", "feb", "29"], ["day"]),
            (ProgressiveDateForm, ["2004", "feb", "29"], []),
        ]
        with app.test_request_context():
            for form_class, values, expected in cases:
                with self.subTest(form=form_class.__name__, values=values):
                    form = form_class()
                    formdata = MultiDict(
                        zip(
                            [f"date-{part}" for part in form.date.field_codes(True)],
                            values,
                            strict=False,
                        )
                    )
                    form.process(formdata=formdata)
                    assert form.date.invalid_parts == expected

    def test_two_digit_year_calendar_validation(self):
        class TwoDigitDateForm(DateInputForm):
            date = TnaDateField(allow_two_digit_year=True)

        with app.test_request_context():
            for year, expected in [("03", ["day"]), ("04", [])]:
                with self.subTest(year=year):
                    form = TwoDigitDateForm(
                        formdata=MultiDict(
                            [
                                ("date-day", "29"),
                                ("date-month", "02"),
                                ("date-year", year),
                            ]
                        )
                    )
                    assert form.date.invalid_parts == expected

    def test_invalid_parts_reset_on_reprocessing(self):
        with app.test_request_context():
            for form_class in (
                DateInputForm,
                MonthInputForm,
                YearInputForm,
                ProgressiveDateForm,
            ):
                with self.subTest(form=form_class.__name__):
                    form = form_class()
                    invalid_data = MultiDict(
                        (f"date-{part}", "invalid")
                        for part in form.date.field_codes(True)
                    )
                    form.process(formdata=invalid_data)
                    assert form.date.invalid_parts
                    valid_data = MultiDict(
                        (
                            f"date-{part}",
                            {"day": "01", "month": "02", "year": "2003"}[part],
                        )
                        for part in form.date.field_codes(True)
                    )
                    form.process(formdata=valid_data)
                    assert form.date.invalid_parts == []
                    form.process(formdata=invalid_data)
                    assert form.date.invalid_parts
                    form.process(
                        formdata=None, data={"date": datetime.date(2003, 2, 1)}
                    )
                    assert form.date.invalid_parts == []
                    assert form.date.data == datetime.date(2003, 2, 1)


class TestMonthInputField(unittest.TestCase):
    def setUp(self):
        self.error_message_required = "Enter a date"
        self.error_message_invalid = "Enter a real date"

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
        self.error_message_invalid = "Enter a real date"

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
        self.error_message_invalid = "Enter a real date"

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
