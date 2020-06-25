import importlib

from dagster import SolidDefinition


def load_solids(module):
    solid_dict = {}
    for name in dir(module):
        attr = getattr(module, name)
        if isinstance(attr, SolidDefinition):
            solid_dict[name] = attr
    return solid_dict


SOLID_DICT = {
    **load_solids(importlib.import_module('.example', 'cube.solids'))
}
