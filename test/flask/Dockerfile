FROM ghcr.io/nationalarchives/tna-python:latest

COPY --chown=app ./test/flask/pyproject.toml /app/pyproject.toml
COPY --chown=app ./test/flask/poetry.lock /app/poetry.lock
COPY --chown=app ./package.json /app/package.json
COPY --chown=app ./package-lock.json /app/package-lock.json

RUN . tna-nvm; \
    npm i; \
    tna-build

COPY --chown=app ./test/flask/app /app/app

CMD ["tna-run", "app:app"]
