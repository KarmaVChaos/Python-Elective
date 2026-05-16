import cv2
import numpy as np
from .exporter_plugin import DataExporterMeta


class PNGExporter(DataExporterMeta, format_name='png'):
    def export(self, image: np.ndarray, filename: str) -> bool:
        path = filename if filename.lower().endswith('.png') else filename + '.png'
        return cv2.imwrite(path, image)
