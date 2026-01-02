FROM ghcr.io/nationalarchives/tna-python-dev:latest

COPY ./test/flask/pyproject.toml /app/pyproject.toml
COPY ./test/flask/poetry.lock /app/poetry.lock
COPY ./package.json /app/package.json
COPY ./package-lock.json /app/package-lock.json

RUN . tna-nvm; \
    npm i; \
    tna-build

COPY ./test/flask/app /app/app

CMD ["tna-wsgi", "app:app"]
