# registry.py
# Register a processor to process json files
from ast import main
from escli_tool.utils import get_logger


logger = get_logger()


CLASS_REGISTRY = {}

def register_class(cls):
    CLASS_REGISTRY[cls.__name__] = cls
    return cls

def get_class(name):
    if name in CLASS_REGISTRY:
        return CLASS_REGISTRY.get(name)
    logger.warning(f"class: {name} is not registered in the list: {set(CLASS_REGISTRY)}")
    return CLASS_REGISTRY.get(name)

def list_registered_classes():
    return list(CLASS_REGISTRY.keys())


if __name__ == '__main__':
    get_class('sad')