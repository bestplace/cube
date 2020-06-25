from dagster import ModeDefinition, default_executors
from dagster_aws.s3 import s3_resource, s3_plus_default_storage_defs
from dagster_celery.executor_docker import celery_docker_executor


celery_docker_mode = ModeDefinition(
    name='celery-docker',
    executor_defs=default_executors + [celery_docker_executor],
    resource_defs={'s3': s3_resource},
    system_storage_defs=s3_plus_default_storage_defs
)