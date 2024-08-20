FROM ghcr.io/nationalarchives/tna-python-dev:latest

COPY --chown=app . .

RUN tna-build

ENV FLASK_APP="test:app"

CMD ["tna-run", "$FLASK_APP"]