from dagster import DependencyDefinition, SolidInvocation, PipelineDefinition
from dagster.utils import load_yaml_from_path

from cube.solids import SOLID_DICT
from cube.modes import celery_docker_mode
from cube.presets import celery_docker_preset


def get_solid_def(def_name):
    if def_name not in SOLID_DICT:
        raise ValueError(f'Unknown library solid {def_name}')
    return SOLID_DICT[def_name]


def _check_duplicate_alias(alias, alias_set):
    if alias not in alias_set:
        alias_set.add(alias)
    else:
        raise ValueError(f'Duplicate alias or def found: {alias}')


def define_pipeline_from_yaml(pipeline_config):
    if isinstance(pipeline_config, str):
        pipeline_config = load_yaml_from_path(pipeline_config)

    pipeline_name = pipeline_config['name']
    pipeline_description = pipeline_config.get('description')
    solids_config = pipeline_config['solids']

    deps = {}
    solid_defs = set()
    solid_aliases = set()
    for solid_config in solids_config:
        solid_def_name = solid_config['def']
        solid_defs.add(get_solid_def(solid_def_name))

        solid_alias = solid_config.get('alias', solid_def_name)
        _check_duplicate_alias(solid_alias, solid_aliases)

        solid_deps = {}
        for input_name, input_solid in solid_config.get('deps', {}).items():
            if '.' in input_solid:
                input_solid, input_solid_result = input_solid.split('.')
            else:
                input_solid, input_solid_result = input_solid, 'result'

            solid_deps[input_name] = DependencyDefinition(
                solid=input_solid, output=input_solid_result
            )
        deps[SolidInvocation(name=solid_def_name, alias=solid_alias)] = solid_deps

    return PipelineDefinition(
        name=pipeline_name,
        description=pipeline_description,
        solid_defs=list(solid_defs),
        dependencies=deps,
        mode_defs=[celery_docker_mode],
        preset_defs=[celery_docker_preset],
    )
