from abc import ABC, abstractmethod
import numpy as np


class DataProcessorMeta(ABC):
    _registry = {}

    def __init_subclass__(cls, processor_name=None, **kw):
        super().__init_subclass__(**kw)
        if processor_name:
            DataProcessorMeta._registry[processor_name] = cls

    @abstractmethod
    def process(self, image: np.ndarray) -> dict:
        ...

    @classmethod
    def get_plugin(cls, processor_name: str):
        plugin_cls = cls._registry.get(processor_name)
        if not plugin_cls:
            raise ValueError(f"Unknown processor: {processor_name}")
        return plugin_cls()
