# Use Bullseye instead of Buster for active repository support
FROM python:3.10-slim-bullseye

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/app

# We'll use --no-cache-dir to keep the image slim
RUN pip install --no-cache-dir \
    dbt-snowflake \
    apache-airflow \
    astronomer-cosmos

COPY . .

CMD ["dbt", "--version"]