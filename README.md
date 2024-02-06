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

Ensure you application is first on the list. This means you can overwrite the standard templates by creating a template with the same filename in your project.

```py
from flask import Flask
from jinja2 import ChoiceLoader, PackageLoader


def create_app():
    app = Flask(__name__)

    app.jinja_loader = ChoiceLoader(
        [
            PackageLoader("app"),
            PackageLoader("tna_frontend_jinja"),
        ]
    )
```

### Using the templates

```jinja
{% from "components/button/macro.html" import tnaButton -%}

{{ tnaButton({
  'text': 'Save and continue'
}) }}
```

The options available to each component macro can be found in the [National Archives Design System Components](https://nationalarchives.github.io/design-system/components/) documentation.

The included templates are a like-for-like port, the only difference between the Nunjucks examples and their Jinja equivalents is having to quote key names, e.g. `'text'` instead of `text`.

We test each component against its published [component fixtures](https://github.com/nationalarchives/tna-frontend/blob/main/src/nationalarchives/components/button/fixtures.json) to ensure complete compatibility.

## Compatibility with TNA Frontend

| TNA Frontend Jinja    | Compatible TNA Frontend versions           |
| --------------------- | ------------------------------------------ |
| `0.1.11`              | `v0.1.36`                                  |
| `0.1.10`              | `v0.1.34`, `v0.1.35`                       |
| `0.1.9`               | `v0.1.33`                                  |
| `0.1.8`               | `v0.1.31`, `v0.1.32`                       |
| `0.1.7`               | `v0.1.31`, `v0.1.32`                       |
| `0.1.6`               | `v0.1.29-prerelease`, `v0.1.30`            |
| `0.1.0`&ndash;`0.1.5` | [latest from `main` branch when published] |

## Test the templates

```sh
python -m venv venv
python install -r test/requirements.txt
flask --app test run --debug --port 5000
node test-fixtures.mjs
```
