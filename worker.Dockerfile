FROM python:3.6-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl git

RUN curl -sL https://deb.nodesource.com/setup_10.x | bash - && \
    apt-get update && \
    apt-get install -y --no-install-recommends nodejs

RUN pip3 install \
        jupyter \
        jupyterlab==1.2.6 \
        nest_asyncio \
        numpy \
        pandas \
        scipy==1.2.1 \
        xlrd \
        ipywidgets && \
    jupyter nbextension enable --py widgetsnbextension && \
    jupyter labextension install @jupyter-widgets/jupyterlab-manager

COPY build/jupyter_notebook_config.py /root/.jupyter/
COPY build/startup.py /root/.ipython/profile_default/startup/startup.py

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

CMD ["jupyter", "lab", "--allow-root", "--no-browser"]

# If you want to develop dagster and need your code in worker images
# cp -r <dagster_source_path>/python_modules ./
# and uncomment this line:
# COPY python_modules ./dagster/python_modules
