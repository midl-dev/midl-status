FROM python:3.10-bookworm
WORKDIR /app
# Install Poetry
RUN apt-get update && apt-get install -y \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python \
    && cd /usr/local/bin \
    && ln -s /opt/poetry/bin/poetry \
    && poetry config virtualenvs.create false
# Install Python dependencies
COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-root --no-cache
# Copy application into image
COPY . /app
# STATIC_PATH configures nginx to serve static assets directly
ENV \
    POETRY_HOME=/opt/poetry \
    STATIC_PATH=/app/app/static \
    FLASK_ENV=production

CMD ["gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "wsgi"]
