# Custom TNA Frontend Jinja fields

TNA Frontend Jinja comes with some custom WTForms fields.

> These fields do not need a `widget` property defined.

These exist mostly because we handle the date field with three inputs for day, month and year rather than a single input field.

All fields support an optional `invalid_date_error_message` parameter to set the error message when an invalid date is entered. This defaults to "[field name] must be a real date".

## `TnaDateField`

Import: **`tna_frontend_jinja.wtforms.fields.TnaDateField`**

Day, month and year fields

```py
date_of_birth = TnaDateField(
    "Date of birth",
    description="Enter your date of birth in the format DD MM YYYY",
)
```

## `TnaMonthField`

Import: **`tna_frontend_jinja.wtforms.fields.TnaMonthField`**

Month and year fields

```py
month_of_birth = TnaMonthField(
    "Month of birth",
    description="Enter your month of birth in the format MM YYYY",
)
```

## `TnaYearField`

Import: **`tna_frontend_jinja.wtforms.fields.TnaYearField`**

Year field

```py
year_of_birth = TnaYearField(
    "Year of birth",
    description="Enter your year of birth in the format YYYY",
)
```

### Optional two digit year support

Pass the `allow_two_digit_year` parameter to allow support for two digit years.

```py
year_of_birth = TnaYearField(
    "Year of birth",
    allow_two_digit_year=True,
    description="Enter your year of birth in the format YY or YYYY",
)
```

## `TnaProgressiveDateField`

Import: **`tna_frontend_jinja.wtforms.fields.TnaProgressiveDateField`**

Date fields that accept year, year/month or year/month/day

```py
approx_date_of_death = TnaProgressiveDateField(
    "Date of death",
    description="Enter as much of the date as you know; either the year, year and month or the full date",
)
```
