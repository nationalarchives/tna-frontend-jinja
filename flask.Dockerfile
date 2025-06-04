FROM ghcr.io/nationalarchives/tna-python:latest

COPY --chown=app ./test/flask/pyproject.toml /app/pyproject.toml
COPY --chown=app ./test/flask/poetry.lock /app/poetry.lock

RUN tna-build

COPY --chown=app . .

CMD ["tna-run", "test.flask:app"]
