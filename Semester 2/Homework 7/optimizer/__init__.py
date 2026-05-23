import importlib
import pkgutil
import os
from .optimizer import OptimMeta

_discovered = False

class PreProcessing:
    @staticmethod
    def autodiscover_plugins() -> None:
        global _discovered
        if _discovered:
            return
        pkg_path = os.path.dirname(__file__)
        for _, mod_name, _ in pkgutil.iter_modules([pkg_path]):
            if mod_name.startswith("_") or mod_name == "optimizer":
                continue
            importlib.import_module(f".{mod_name}", __package__)
        _discovered = True

# Автозапуск при импорте пакета
PreProcessing.autodiscover_plugins()

__all__ = ["OptimMeta", "PreProcessing"]