FROM ghcr.io/nationalarchives/tna-python-django:latest

COPY --chown=app ./test/django/pyproject.toml /app/pyproject.toml
COPY --chown=app ./test/django/poetry.lock /app/poetry.lock

RUN tna-build

COPY --chown=app . .

CMD ["tna-run", "test.django.wsgi:application"]
