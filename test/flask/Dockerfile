FROM ghcr.io/nationalarchives/tna-python:latest

COPY --chown=app ./pyproject.toml /app/pyproject.toml
COPY --chown=app ./poetry.lock /app/poetry.lock

RUN tna-build

COPY --chown=app ./app /app/app

CMD ["tna-run", "app:app"]
