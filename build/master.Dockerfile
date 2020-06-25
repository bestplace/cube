FROM python:3.6-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends cron curl git

RUN curl -sL https://deb.nodesource.com/setup_10.x | bash - && \
    apt-get update && \
    apt-get install -y --no-install-recommends nodejs && \
    npm install --unsafe-perm -g pm2 yarn

ENV DAGSTER_HOME=/opt/dagster/home
WORKDIR /opt/dagster/app

ARG origin=dagster-io
ARG branch=master
RUN git clone --depth 1 -b $branch https://github.com/$origin/dagster.git && \
    pip install \
        -e dagster/python_modules/dagster \
        -e dagster/python_modules/dagster-graphql \
        -e dagster/python_modules/dagit \
        -e dagster/python_modules/libraries/dagstermill \
        -e dagster/python_modules/libraries/dagster-aws \
        -e dagster/python_modules/libraries/dagster-celery \
        -e dagster/python_modules/libraries/dagster-postgres && \
    cd dagster/js_modules/dagit && \
    yarn install && yarn build-for-python

COPY master.process.yml process.yml
COPY cronstart workspace.yaml ./
COPY dagster.yaml /opt/dagster/home/dagster.yaml

ENTRYPOINT ["pm2-docker", "process.yml"]
