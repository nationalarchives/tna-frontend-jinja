# TNA WTForms fields

TNA Frontend Jinja comes with some custom WTForms fields.

> These fields do not need a `widget` property defined.

These exist mostly because we handle the date field with three inputs for day, month and year rather than a single input field.

All fields support an optional `invalid_date_error_message` parameter to set the error message when an invalid date is entered. This defaults to "[field name] must be a real date".

## Date fields

### `TnaDateField`

Import: **`tna_frontend_jinja.wtforms.fields.TnaDateField`**

Day, month and year fields

```py
date_of_birth = TnaDateField(
    "Date of birth",
    description="Enter your date of birth in the format DD MM YYYY",
)
```

## Partial date fields

### `TnaMonthField`

Import: **`tna_frontend_jinja.wtforms.fields.TnaMonthField`**

Month and year fields

```py
month_of_birth = TnaMonthField(
    "Month of birth",
    description="Enter your month of birth in the format MM YYYY",
)
```

### `TnaYearField`

Import: **`tna_frontend_jinja.wtforms.fields.TnaYearField`**

Year field

```py
year_of_birth = TnaYearField(
    "Year of birth",
    description="Enter your year of birth in the format YYYY",
)
```

### `TnaProgressiveDateField`

Import: **`tna_frontend_jinja.wtforms.fields.TnaProgressiveDateField`**

Date fields that accept year, year/month or year/month/day

```py
approx_date_of_death = TnaProgressiveDateField(
    "Date of death",
    description="Enter as much of the date as you know; either the year, year and month or the full date",
)
```

### Options

#### Two digit year support

Pass `allow_two_digit_year=True` parameter to enable support for two digit years in partial date fields.

```py
year_of_birth = TnaYearField(
    "Year of birth",
    description="Enter your year of birth in the format YY or YYYY",
    allow_two_digit_year=True,
)
```

#### Coerce partial date to the end of its range

Pass `end_of_partial_date_range=True` parameter to coerse a partial date to the end of its range.

| Inputs           | `end_of_partial_date_range=False` (default) | `end_of_partial_date_range=True` |
| ---------------- | ------------------------------------------- | -------------------------------- |
| `2003`           | `Wed, 01 Jan 2003 00:00:00 GMT`             | `Wed, 31 Dec 2003 23:59:59 GMT`  |
| `2003`, `9`      | `Mon, 01 Sep 2003 00:00:00 GMT`             | `Tue, 30 Sep 2003 23:59:59 GMT`  |
| `2003`, `9`, `2` | `Tue, 02 Sep 2003 00:00:00 GMT`             | `Tue, 02 Sep 2003 23:59:59 GMT`  |

```py
# Will result in 1 Jan for the given year
start = TnaYearField(
    "Record start year",
    description="Enter the starting year",
)

# Will result in 31 Dec for the given year
end = TnaYearField(
    "Record end year",
    description="Enter the ending year",
    end_of_partial_date_range=True,
)
```
