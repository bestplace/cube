# CUBE

## Dagster + Celery + DinD + S3 + Postgres

This is a boilerplate repo for setting up your scalable dagster deployment using docker and ansible

Disclaimer: `Currently DinD Executor is experimental and only available in bestplace/dagster`

### Structure

```bash
├── README.md
├── build
│   ├── celery_config.yaml
│   ├── cronstart
│   ├── dagster.yaml
│   ├── int2term
│   ├── master.Dockerfile
│   ├── master.process.yml
│   ├── runner.Dockerfile
│   ├── runner.process.yml
│   └── workspace.yaml
├── cube
│   ├── modes.py
│   ├── pipelines
│   │   ├── __init__.py
│   │   ├── example.py
│   │   └── example.yml
│   ├── presets.py
│   ├── repository.py
│   └── solids
│       ├── __init__.py
│       └── example.py
├── roles
│   └── dagster
│       ├── defaults
│       │   └── main.yml
│       ├── handlers
│       │   └── main.yml
│       ├── tasks
│       │   └── main.yml
│       └── templates
│           └── docker-compose.yml
├─* devel.ini
├─* python_modules
├── hosts.yml
├── local.yml
├── docker-compose.yml
└── worker.Dockerfile
```

### Code

All the code is located in `cube` folder

It has a single repository called `cube` in `repository.py`. This repository automatically collects all pipelines from the `pipelines` folder, so you don't need to manually add new pipelines to repo each time, you can just commit new .py or .yaml files to this folder and after deploy they will be immediately visible in your dagit interface.

Pipelines can be defined in 2 ways:
* python code (https://docs.dagster.io/docs/tutorial/basics_pipelines)
* or yaml DSL (similar to https://github.com/dagster-io/dagster/tree/master/examples/dep_dsl but with an additional dot-syntax for multiple outputs)

Solids are located in `solids` folder and all of the are automatically parsed and made available to yaml pipelines. Currently we maintain only .py solids but we'll include .ipynb soon.

At last there is a predefined mode in `modes.py` for celery-docker execution and a luanch preset in `presets.py` which is configured at runtime from env.

### Build

The whole deployment set consists of 6 containers:

* `cube-storage`  - s3 storage for intermediates and compute logs (we use zenko/cloudserver because at the moment for some API reasons minio works 11x times slower)
* `cube-rabbitmq` - RabbitMQ broker for Celery executor
* `cube-postgres` - PostgreSQL DB for run, schedule and event log storage
* `cube-master`   - dagit server (launches runs in separate processes in the same container)
* `cube-runner`   - a bunch of dagster-celery worker containers (accept tasks and spawn worker containers)
* `cube-worker`   - versioned docker containers to run your pipelines code

All of master, runner and worker are built with docker-compose file at root

It accepts several config variables from env:
~~~
DOCKER_REGISTRY - your docker registry (must be the same as in your hosts.yml, default=cube)
VERSION_TAG     - image version tag (default=latest)
ORIGIN / BRANCH - dagster github repository for building your containers (default=dagster-io / master)
~~~

Example:
`Currently DinD Executor is experimental and is only available in bestplace/dagster`
```
ORIGIN=bestplace BRANCH=bestplace docker-compose build
```

### Deploy

Disclaimer: `Local deployment was only tested on OSX. You'll have to change app_host to 172.17.0.1 in your local.yml to run it on linux machine and who knows what else`

The deployment is configured and orchestrated by `ansible`

We have a `dagster` role in `roles` folder that prepares a `docker-compose.yml`, rsyncs all the code and runs it localy or on a remote server.

Running it locally is as easy as:

~~~
# generate new docker-compose.yml, rsync everything and deploy new containers
DEPLOY=yes ansible-playbook local.yml

# only rsync new code (it will automatically hot-reload master and runners)
ansible-playbook local.yml
~~~

It will create _dagster folder with all the necessary stuff inside

You can look at all the playbook options in `roles/dagster/defaults/main.yml`

### Init Storage

Dagster needs a bucket to be created before it can be used

* download aws client (https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-mac.html)
* follow this instruction to create credentials config - defaults are `cube:cube` (https://s3-server.readthedocs.io/en/latest/CLIENTS.html)
* `aws --endpoint-url=http://localhost:8000 s3 mb s3://dagster`

### Developing dagster

You can sourcemap dagster code into your local deployment and it will hot-reload on changes

Create `devel.ini` file with this content
~~~
[default]
dagster_devel_path=/path/to/dagster/repo
~~~

Then redeploy your playbook.

If you need to propogate code changes to your worker containers you go as follows:
* cp -r /path/to/dagster/repo/python_modules ./
* uncomment the last line in worker.Dockerfile
* rebuild (docker-compose build)

### Example pipelines run configs

Now when everything is ready you can open dagit in your browser (localhost:3000)

Select one of the piplines and go to playground. Select celery-docker preset and paste one of the appropriate configs below

#### example_add_pipeline
~~~
solids:
  example_add_x:
    config:
      x: 1
    inputs:
      num: 3
  example_add_one:
    inputs:
      num: 3
~~~

#### example_yaml_pipeline
~~~
solids:
  add_x:
    config:
      x: 1
    inputs:
      num: 3
  example_add_one:
    inputs:
      num: 3
~~~

and launch!
