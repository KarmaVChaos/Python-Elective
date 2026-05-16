from abc import ABC, abstractmethod
import numpy as np


class DataExporterMeta(ABC):
    _registry = {}

    def __init_subclass__(cls, format_name=None, **kw):
        super().__init_subclass__(**kw)
        if format_name:
            DataExporterMeta._registry[format_name] = cls

    @abstractmethod
    def export(self, image: np.ndarray, filename: str) -> bool:
        ...

    @classmethod
    def get_plugin(cls, format_name: str):
        plugin_cls = cls._registry.get(format_name)
        if not plugin_cls:
            raise ValueError(f"Unknown export format: {format_name}")
        return plugin_cls()
