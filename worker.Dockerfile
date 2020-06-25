FROM docker.bestplace.tech/bestplace/judo:v0.0.121

ENV DAGSTER_HOME=/opt/dagster/home
WORKDIR /opt/dagster/app

ARG origin=dagster-io
ARG branch=master
RUN git clone --depth 1 -b $branch https://github.com/$origin/dagster.git && \
    pip install \
        -e dagster/python_modules/dagster \
        -e dagster/python_modules/dagster-graphql \
        -e dagster/python_modules/libraries/dagstermill \
        -e dagster/python_modules/libraries/dagster-aws \
        -e dagster/python_modules/libraries/dagster-celery \
        -e dagster/python_modules/libraries/dagster-postgres

COPY build/dagster.yaml /opt/dagster/home/dagster.yaml
COPY build/workspace.yaml ./
COPY cube ./cube

# If you want to develop dagster and need your code in worker images
# cp -r <dagster_source_path>/python_modules ./
# and uncomment this line:
# COPY python_modules ./dagster/python_modules