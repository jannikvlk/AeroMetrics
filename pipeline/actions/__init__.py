import importlib
import pkgutil

# Iterate through the modules in the 'actions' package
for loader, module_name, is_pkg in pkgutil.iter_modules(__path__):
    full_module_name = f"{__name__}.{module_name}"
    try:
        module = importlib.import_module(full_module_name)
        setattr(globals(), module_name, module)
    except Exception as e:
        print(f"Failed to import module {full_module_name}: {e}")
