from dagster import solid, Output, OutputDefinition, Field, Int
from time import sleep


@solid
def example_info(context, value: int):
    sleep(1)
    context.log.info(f'Example log: {value}')


@solid
def example_add_one(_, num: int) -> int:
    sleep(1)
    return num + 1


@solid(
    config_schema={
        'x': Field(Int, is_required=True, description='Num to add')
    }
)
def example_add_x(context, num: int) -> int:
    x = context.solid_config['x']
    sleep(1)
    context.log.info(f'Add {x} to input num {num}')
    return num + x


@solid
def example_add(context, left: int, right: int) -> int:
    sleep(1)
    context.log.info(f'Return sum of input values: {left}, {right}')
    return left + right


@solid(
    output_defs=[
        OutputDefinition(name='sum', dagster_type=Int, is_required=True),
        OutputDefinition(name='product', dagster_type=Int, is_required=True),
    ]
)
def example_add_mul(context, left: int, right: int) -> int:
    sleep(1)
    context.log.info(f'Return sum and product of input values: {left}, {right}')
    yield Output(left + right, 'sum')
    yield Output(left * right, 'product')


