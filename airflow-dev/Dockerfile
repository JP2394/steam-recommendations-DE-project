FROM quay.io/astronomer/astro-runtime:10.6.0

USER root
RUN apt-get clean && \
    apt-get update && \
    apt-get install -y unzip

# install dbt into a virtual environment
RUN python -m venv dbt_venv && source dbt_venv/bin/activate && \
    pip install --no-cache-dir dbt-bigquery && deactivate


ENV KAGGLE_USERNAME=josedanielplasencia
ENV KAGGLE_KEY=040136148472ee4bd97d4a016bfe5709