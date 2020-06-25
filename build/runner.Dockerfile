FROM python:3.6-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl git

RUN curl -sL https://deb.nodesource.com/setup_10.x | bash - && \
    apt-get update && \
    apt-get install -y --no-install-recommends nodejs && \
    npm install --unsafe-perm -g pm2

ENV DAGSTER_HOME=/opt/dagster/home
WORKDIR /opt/dagster/app

ARG origin=dagster-io
ARG branch=master
RUN git clone --depth 1 -b $branch https://github.com/$origin/dagster.git && \
    pip install \
        -e dagster/python_modules/dagster[docker] \
        -e dagster/python_modules/dagster-graphql \
        -e dagster/python_modules/libraries/dagstermill \
        -e dagster/python_modules/libraries/dagster-aws \
        -e dagster/python_modules/libraries/dagster-celery \
        -e dagster/python_modules/libraries/dagster-postgres

COPY runner.process.yml process.yml
COPY int2term workspace.yaml celery_config.yaml ./
COPY dagster.yaml /opt/dagster/home/dagster.yaml

ENTRYPOINT ["pm2-docker", "process.yml"]
