import os
import sys
from functools import partial

from dagster import repository
from dagster.utils import file_relative_path, load_yaml_from_path
from dagster.cli.workspace.autodiscovery import loadable_targets_from_python_file

from cube.pipelines import define_pipeline_from_yaml


PIPELINES_DIR = 'pipelines'


def get_pipelines():
    pipelines = {}
    for filename in os.listdir(file_relative_path(__file__, PIPELINES_DIR)):
        if filename.endswith('.yml') or filename.endswith('.yaml'):
            yaml_config = load_yaml_from_path(file_relative_path(__file__, f'{PIPELINES_DIR}/{filename}'))
            pipeline_name = yaml_config['name']
            pipelines[pipeline_name] = partial(define_pipeline_from_yaml, yaml_config)
        elif filename.endswith('.py') and filename != '__init__.py':
            targets = loadable_targets_from_python_file(file_relative_path(__file__, f'{PIPELINES_DIR}/{filename}'))
            for target in targets:
                pipelines[target.attribute] = target.target_definition
    return pipelines


@repository
def cube():
    return {'pipelines': get_pipelines()}
