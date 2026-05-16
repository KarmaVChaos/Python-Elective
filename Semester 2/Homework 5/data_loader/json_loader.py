import json
import os
import random
from pathlib import Path

import cv2
import numpy as np

from .loader_plugin import DataLoaderMeta


class JSONLoader(DataLoaderMeta, format_name='json'):
    def validate(self, filename: str) -> bool:
        p = Path(filename)
        if not p.exists():
            raise FileNotFoundError(f'File not found: {p}')
        if p.stat().st_size == 0:
            raise ValueError(f'File is empty: {p}')
        return p.suffix.lower() == '.json'

    def load(self, filename: str) -> np.ndarray:
        if not self.validate(filename):
            return None

        with open(filename, 'r') as f:
            cfg = json.load(f)

        w, h = cfg.get('image_size', [256, 256])
        grayscale = cfg.get('color_mode', 'RGB').lower() == 'grayscale'
        num_objects = cfg.get('num_objects', 3)
        allow_overlap = cfg.get('allow_overlap', True)
        bg_path = cfg.get('background_path', '')
        obj_path = cfg.get('objects_path', '')

        canvas = self._load_background(bg_path, w, h, grayscale)
        placed = []
        obj_imgs = self._collect_images(obj_path)

        for _ in range(num_objects * 20):
            if len(placed) >= num_objects:
                break
            obj = self._get_object(obj_imgs, grayscale)
            oh, ow = obj.shape[:2]
            if ow > w or oh > h:
                obj = cv2.resize(obj, (min(ow, w // 2), min(oh, h // 2)))
                oh, ow = obj.shape[:2]
            x = random.randint(0, w - ow)
            y = random.randint(0, h - oh)
            rect = (x, y, ow, oh)
            if not allow_overlap and self._overlaps(rect, placed):
                continue
            self._paste(canvas, obj, x, y)
            placed.append(rect)

        if grayscale and len(canvas.shape) == 3:
            canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)

        return canvas

    def _load_background(self, bg_path, w, h, grayscale):
        imgs = self._collect_images(bg_path)
        if imgs:
            bg = cv2.resize(cv2.imread(random.choice(imgs)), (w, h))
            if grayscale:
                bg = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)
                bg = cv2.cvtColor(bg, cv2.COLOR_GRAY2BGR)
            return bg
        color = [random.randint(100, 200) for _ in range(3)]
        return np.full((h, w, 3), color, dtype=np.uint8)

    def _collect_images(self, folder):
        if not folder or not os.path.isdir(folder):
            return []
        exts = {'.png', '.jpg', '.jpeg', '.bmp'}
        return [
            os.path.join(folder, f)
            for f in os.listdir(folder)
            if Path(f).suffix.lower() in exts
        ]

    def _get_object(self, obj_imgs, grayscale):
        if obj_imgs:
            img = cv2.imread(random.choice(obj_imgs))
        else:
            size = random.randint(20, 60)
            color = [random.randint(0, 255) for _ in range(3)]
            img = np.full((size, size, 3), color, dtype=np.uint8)
        if grayscale and len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        return img

    def _overlaps(self, rect, placed):
        x, y, w, h = rect
        for px, py, pw, ph in placed:
            if x < px + pw and x + w > px and y < py + ph and y + h > py:
                return True
        return False

    def _paste(self, canvas, obj, x, y):
        oh, ow = obj.shape[:2]
        roi = canvas[y:y + oh, x:x + ow]
        mask = np.any(obj != canvas[y:y + oh, x:x + ow], axis=-1) if len(obj.shape) == 3 else obj != canvas[y:y + oh, x:x + ow]
        roi[mask] = obj[mask]
