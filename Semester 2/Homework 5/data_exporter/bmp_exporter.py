import cv2
import numpy as np
from .exporter_plugin import DataExporterMeta


class BMPExporter(DataExporterMeta, format_name='bmp'):
    def export(self, image: np.ndarray, filename: str) -> bool:
        path = filename if filename.lower().endswith('.bmp') else filename + '.bmp'
        return cv2.imwrite(path, image)
