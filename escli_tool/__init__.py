import pkgutil
import importlib
import escli_tool.data_processor

for _, module_name, _ in pkgutil.iter_modules(escli_tool.data_processor.__path__):
    importlib.import_module(f"escli_tool.data_processor.{module_name}")