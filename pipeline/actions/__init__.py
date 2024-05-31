import os
import importlib

# List all Python files in the current directory
module_dir = os.path.dirname(__file__)
module_files = [
    f for f in os.listdir(module_dir) if f.endswith(".py") and f != "__init__.py"
]

# Dynamically import all modules and add them to the current namespace
for module_file in module_files:
    module_name = module_file[:-3]  # Remove the .py extension
    module = importlib.import_module(f".{module_name}", package=__name__)
    globals()[module_name] = module
