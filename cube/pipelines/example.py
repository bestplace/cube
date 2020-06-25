from dagster import pipeline

from cube.solids.example import example_info, example_add_one, example_add_x, example_add_mul
from cube.modes import celery_docker_mode
from cube.presets import celery_docker_preset


@pipeline(mode_defs=[celery_docker_mode], preset_defs=[celery_docker_preset])
def example_add_pipeline():
    res_sum, res_prod = example_add_mul(example_add_one(), example_add_x())
    example_info(res_sum)
    example_info(res_prod)
