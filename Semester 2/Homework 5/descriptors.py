import os
import numpy as np
import cv2


class NotEmptyFile:
    def __set_name__(self, owner, name):
        self._attr = '_' + name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self._attr, None)

    def __set__(self, obj, value):
        if isinstance(value, str) and os.path.isfile(value):
            if os.path.getsize(value) == 0:
                raise ValueError(f"File '{value}' is empty")
        setattr(obj, self._attr, value)


class ColorCountValidator:
    MIN_COLORS = 2

    def __set_name__(self, owner, name):
        self._attr = '_' + name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self._attr, None)

    def __set__(self, obj, value):
        if isinstance(value, np.ndarray) and value.size > 0:
            channels = value.shape[-1] if len(value.shape) == 3 else 1
            flat = value.reshape(-1, channels)
            n_colors = len(np.unique(flat, axis=0))
            if n_colors <= self.MIN_COLORS:
                raise ValueError(
                    f"Image has {n_colors} unique color(s); must have more than {self.MIN_COLORS}"
                )
        setattr(obj, self._attr, value)


class AutoResizeImage:
    SIZE = (256, 256)

    def __set_name__(self, owner, name):
        self._attr = '_' + name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self._attr, None)

    def __set__(self, obj, value):
        if isinstance(value, np.ndarray):
            value = cv2.resize(value, self.SIZE)
        elif isinstance(value, str):
            img = cv2.imread(value)
            if img is None:
                raise ValueError(f"Cannot read image from '{value}'")
            value = cv2.resize(img, self.SIZE)
        setattr(obj, self._attr, value)


class ValidatedImage:
    file_path = NotEmptyFile()
    image = AutoResizeImage()
    validated_image = ColorCountValidator()

    def load(self, path: str) -> np.ndarray:
        self.file_path = path
        self.image = path
        self.validated_image = self.image
        return self.validated_image
