# Custom TNA WTForms validators

## Date validators

Compatible with:

- [`TnaDateField`](./tna-fields.md#tnadatefield)
- [`TnaMonthField`](./tna-fields.md#tnamonthfield)
- [`TnaYearField`](./tna-fields.md#tnayearfield)
- [`TnaProgressiveDateField`](./tna-fields.md#tnaprogressivedatefield)

### `FutureDate`

Import: **`tna_frontend_jinja.wtforms.validators.FutureDate`**

```py
year_of_retirement = TnaYearField(
    "Planned year of retirement",
    description="Enter your planned year of retirement in the format YYYY",
    invalid_date_error_message="Planned year of retirement must be a valid year",
    include_today=True,  # The current year is a valid option
    validators=[
        validators.InputRequired(message="Enter a year for retirement"),
        tna_frontend_validators.FutureDate(
            message="Year of retirement must be in the future"
        ),
    ],
)
```

### `PastDate`

Import: **`tna_frontend_jinja.wtforms.validators.PastDate`**

```py
year_birth = TnaYearField(
    "Year of birth",
    description="Enter your year of birth in the format YYYY",
    invalid_date_error_message="Year of birth must be a valid year",
    include_today=False,  # Don't consider the current year valid
    validators=[
        validators.InputRequired(message="Enter a year of birth"),
        tna_frontend_validators.PastDate(
            message="Year year of birth must be in the past"
        ),
    ],
)
```

## Checkbox validators

Compatible with:

- [`SelectMultipleField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.SelectMultipleField)

### `MaxOptions`

Import: **`tna_frontend_jinja.wtforms.validators.MaxOptions`**

```py
contact_preference = SelectMultipleField(
    "Contact preference",
    description="Select up to two methods of contact",
    validators=[
        validators.InputRequired(message="Select at least one item"),
        tna_frontend_validators.MaxOptions(
            max=2,
            message="You must select no more than 2 items"
        ),
    ],
    choices=[("phone", "Phone"), ("email", "Email"), ("sms", "SMS")],
    widget=TnaCheckboxesWidget(),
)
```
