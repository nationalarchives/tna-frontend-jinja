# TNA WTForms field widgets

| WTForms field                                                                                               | TNA widget(s)                                                             |
| ----------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| [`BooleanField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.BooleanField)               | ✅ `TnaCheckboxWidget`                                                    |
| [`ColorField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.ColorField)                   | 🔧 [not yet supported]                                                    |
| [`DateField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.DateField)                     | ❌ [not supported] - use [`TnaDateField`](./tna-fields.md#tnadatefield)   |
| [`DateTimeField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.DateTimeField)             | 🔧 [not yet supported]                                                    |
| [`DateTimeLocalField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.DateTimeLocalField)   | 🔧 [not yet supported]                                                    |
| [`DecimalField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.DecimalField)               | ✅ `TnaNumberInputWidget`                                                 |
| [`DecimalRangeField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.DecimalRangeField)     | 🔧 [not yet supported]                                                    |
| [`EmailField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.EmailField)                   | ✅ `TnaEmailInputWidget`                                                  |
| [`FieldList`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.FieldList)                     | 🔧 [not yet supported]                                                    |
| [`FileField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.FileField)                     | ✅ `TnaFileInputWidget` or `TnaDroppableFileInputWidget`                  |
| [`FloatField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.FloatField)                   | ✅ `TnaNumberInputWidget`                                                 |
| [`FormField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.FormField)                     | 🔧 [not yet supported]                                                    |
| [`HiddenField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.HiddenField)                 | ✅ [none needed]                                                          |
| [`IntegerField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.IntegerField)               | ✅ `TnaNumberInputWidget`                                                 |
| [`IntegerRangeField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.IntegerRangeField)     | 🔧 [not yet supported]                                                    |
| [`MultipleFileField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.MultipleFileField)     | ✅ `TnaFilesInputWidget` or `TnaDroppableFilesInputWidget`                |
| [`MonthField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.MonthField)                   | ❌ [not supported] - use [`TnaMonthField`](./tna-fields.md#tnamonthfield) |
| [`PasswordField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.PasswordField)             | ✅ `TnaPasswordWidget`                                                    |
| [`RadioField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.RadioField)                   | ✅ `TnaRadiosWidget`                                                      |
| [`SelectField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.SelectField)                 | ✅ `TnaSelectWidget`                                                      |
| [`SearchField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.SearchField)                 | ✅ `TnaSearchFieldWidget`                                                 |
| [`SelectMultipleField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.SelectMultipleField) | ✅ `TnaCheckboxesWidget`                                                  |
| [`SubmitField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.SubmitField)                 | ✅ `TnaSubmitWidget`                                                      |
| [`StringField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.StringField)                 | ✅ `TnaTextInputWidget`                                                   |
| [`TelField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.TelField)                       | ✅ `TnaTelInputWidget`                                                    |
| [`TimeField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.TimeField)                     | 🔧 [not yet supported]                                                    |
| [`TextAreaField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.TextAreaField)             | ✅ `TnaTextareaWidget`                                                    |
| [`URLField`](https://wtforms.readthedocs.io/en/3.1.x/fields/#wtforms.fields.URLField)                       | ✅ `TnaUrlInputWidget`                                                    |
