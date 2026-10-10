FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    AV_VALIDATOR_MAX_SCENE_BYTES=2000000 \
    AV_VALIDATOR_OUTPUT_FORMAT=text

WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
RUN python -m pip install --no-cache-dir . \
    && useradd --create-home --uid 10001 validator

COPY --chown=validator:validator rules ./rules
COPY --chown=validator:validator sample-configs ./sample-configs
USER validator

ENTRYPOINT ["python", "-m", "av_validator"]
