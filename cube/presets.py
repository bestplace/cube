import os
from dagster import PresetDefinition


APP_HOST = os.environ.get('APP_HOST', 'docker.for.mac.localhost')
WORKER_IMAGE = os.environ.get('WORKER_IMAGE', 'busybox:latest')


celery_docker_preset = PresetDefinition(
    'celery-docker',
    run_config={
        'execution': {
            'celery-docker': {
                'config': {
                    'broker': f'amqp://guest:guest@{APP_HOST}:5672//',
                    'docker_image': WORKER_IMAGE,
                    'repo_location_name': 'bestplace',
                }
            }
        },
        'resources': {
            's3': {
                'config': {
                    'endpoint_url': f'http://{APP_HOST}:8000'
                }
            }
        },
        'storage': {
            's3': {
                'config': {
                    's3_bucket': 'dagster'
                }
            }
        }
    },
    mode='celery-docker'
)
