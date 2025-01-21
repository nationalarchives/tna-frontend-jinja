<img src="https://raw.githubusercontent.com/nationalarchives/tna-frontend/main/src/nationalarchives/assets/images/tna-square-logo.svg" alt="The National Archives logo" title="The National Archives" width="100" />

# TNA Frontend Jinja

[![Main build status](https://img.shields.io/github/actions/workflow/status/nationalarchives/tna-frontend-jinja/ci.yml?style=flat-square&event=push&branch=main)](https://github.com/nationalarchives/tna-frontend-jinja/actions/workflows/ci.yml?query=branch%3Amain)
[![Latest release](https://img.shields.io/github/v/release/nationalarchives/tna-frontend-jinja?style=flat-square&logo=github&logoColor=white&sort=semver)](https://github.com/nationalarchives/tna-frontend-jinja/releases)
[![PyPi version](https://img.shields.io/pypi/v/tna-frontend-jinja?style=flat-square&logo=pypi&logoColor=white)](https://pypi.org/project/tna-frontend-jinja/)
![Python version](https://img.shields.io/pypi/pyversions/tna-frontend-jinja?style=flat-square&logo=python&logoColor=white)
[![Licence](https://img.shields.io/github/license/nationalarchives/tna-frontend-jinja?style=flat-square)](https://github.com/nationalarchives/tna-frontend-jinja/blob/main/LICENCE)

TNA Frontend Jinja templates are a [Jinja](https://jinja.palletsprojects.com/en/3.1.x/) implementation of the templates provided as part of [TNA Frontend](https://github.com/nationalarchives/tna-frontend).

## Quickstart for Flask projects

Use the Flask application's `jinja_loader` to allow templates included from either your app (in the below example called `app`) and the `tna_frontend_jinja` package.

Ensure your application is first on the list. This means you can [overwrite the standard templates](#overriding-templates) by creating a template with the same filename in your project.

```py
from flask import Flask
from jinja2 import ChoiceLoader, PackageLoader


def create_app():
    app = Flask(__name__)

    app.jinja_loader = ChoiceLoader(
        [
            PackageLoader("app"),  # Use your application directory here
            PackageLoader("tna_frontend_jinja"),
        ]
    )
```

## Quickstart for Django projects

Update the `TEMPLATES` setting in your application config:

```py
TEMPLATES = [
    # Add the Jinja2 backend first
    {
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        "DIRS": [
            os.path.join(BASE_DIR, "app/templates"),  # Use your application directory here
            os.path.join(get_path("platlib"), "tna_frontend_jinja/templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "environment": "config.jinja2.environment",
        },
    },
    # The DjangoTemplates backend is still needed for tools like Django admin and the debug toolbar
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
```

Ensure your application is first on the list of template directories. This means you can [overwrite the standard templates](#overriding-templates) by creating a template with the same filename in your project.

## Using the templates

```jinja
{% from 'components/button/macro.html' import tnaButton %}

{{ tnaButton({
  'text': 'Save and continue'
}) }}
```

The options available to each component macro can be found in the [National Archives Design System Components](https://nationalarchives.github.io/design-system/components/) documentation.

The included templates are a like-for-like port, the only difference between the Nunjucks examples and their Jinja equivalents is having to quote key names, e.g. `'text'` instead of `text`.

We test each component against its published [component fixtures](https://github.com/nationalarchives/tna-frontend/blob/main/src/nationalarchives/components/button/fixtures.json) to ensure complete compatibility.

### Overriding templates

To make modifications to the templates, create a new file in your applciation templates directory with the same name as the template you want to customise.

For example, if your application templates directory is `app/templates`, create `app/templates/components/button/macro.html` and insert your own HTML using the same macro name (e.g. `tnaButton`).

This way you can continue to use the same import (e.g. `{% from 'components/button/macro.html' import tnaButton %}`) but introduce your own bespoke functionality.

## Testing the templates

```sh
docker compose up -d
npm install
node test-fixtures.mjs
```

## Styles and JavaScript

The CSS and JavaScript are not included in the PyPI package. You must install them separately.

Install and use the `@nationalarchives/frontend` package from npm with `npm install @nationalarchives/frontend`.

Ensure you install the correct version of TNA Frontend for the version of the templates you are using.

### Compatibility with TNA Frontend

#### v0.3+

| TNA Frontend Jinja | Compatible TNA Frontend version(s) |
| ------------------ | ---------------------------------- |
| `0.8.1`            | `0.8.1`                            |
| `0.8.0`            | `0.8.0`                            |
| `0.7.0`            | `0.7.0`, `0.7.1`, `0.7.2`          |
| `0.6.0`            | `0.6.0`                            |
| `0.5.0`            | `0.5.0`                            |
| `0.4.0`            | `0.4.0`                            |
| `0.3.0`            | `0.3.0`                            |

#### v0.2.x

| TNA Frontend Jinja | Compatible TNA Frontend version(s) |
| ------------------ | ---------------------------------- |
| `0.2.18`           | `0.2.18`                           |
| `0.2.17`           | `0.2.17`                           |
| `0.2.16`           | `0.2.16`                           |
| `0.2.15`           | `0.2.15`                           |
| `0.2.14`           | `0.2.14`                           |
| `0.2.13`           | `0.2.13`                           |
| `0.2.12`           | `0.2.12`                           |
| `0.2.11`           | `0.2.11`                           |
| `0.2.10`           | `0.2.10`                           |
| `0.2.9`            | `0.2.9`                            |
| `0.2.8`            | `0.2.8`                            |
| `0.2.7`            | `0.2.7`                            |
| `0.2.6`            | `0.2.6`                            |
| `0.2.5`            | `0.2.5`                            |
| `0.2.4`            | `0.2.4`                            |
| `0.2.3`            | `0.2.3`                            |
| `0.2.2`            | `0.2.2`                            |
| `0.2.1`            | `0.2.1`                            |
| `0.2.0`            | `0.2.0`                            |

#### v0.1.x

| TNA Frontend Jinja    | Compatible TNA Frontend version(s)         |
| --------------------- | ------------------------------------------ |
| `0.1.34`              | `0.1.65`                                   |
| `0.1.33`              | `0.1.62`, `0.1.63`, `0.1.64`               |
| `0.1.32`              | `0.1.60`, `0.1.61`                         |
| `0.1.31`              | `0.1.59`                                   |
| `0.1.30`              | `0.1.58`                                   |
| `0.1.29`              | `0.1.57`                                   |
| `0.1.28`              | `0.1.55`, `0.1.56`                         |
| `0.1.27`              | `0.1.54`                                   |
| `0.1.26`              | `0.1.53`                                   |
| `0.1.25`              | `0.1.51`, `0.1.52`                         |
| `0.1.23`, `0.1.24`    | `0.1.50`                                   |
| `0.1.21`, `0.1.22`    | `0.1.49`                                   |
| `0.1.20`              | `0.1.48`                                   |
| `0.1.19`              | `0.1.45`, `0.1.46`, `0.1.47`               |
| `0.1.18`              | `0.1.44`                                   |
| `0.1.17`              | `0.1.43`                                   |
| `0.1.15`, `0.1.16`    | `0.1.42`                                   |
| `0.1.14`              | `0.1.40`, `0.1.41`                         |
| `0.1.13`              | `0.1.39`                                   |
| `0.1.12`              | `0.1.37`, `0.1.38`                         |
| `0.1.11`              | `0.1.36`                                   |
| `0.1.10`              | `0.1.34`, `0.1.35`                         |
| `0.1.9`               | `0.1.33`                                   |
| `0.1.7`, `0.1.8`      | `0.1.31`, `0.1.32`                         |
| `0.1.6`               | `0.1.29-prerelease`, `0.1.30`              |
| `0.1.0`&ndash;`0.1.5` | [latest from `main` branch when published] |
