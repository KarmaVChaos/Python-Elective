import cv2
import numpy as np
from .exporter_plugin import DataExporterMeta


class JPGExporter(DataExporterMeta, format_name='jpg'):
    def export(self, image: np.ndarray, filename: str) -> bool:
        path = filename if filename.lower().endswith(('.jpg', '.jpeg')) else filename + '.jpg'
        return cv2.imwrite(path, image, [cv2.IMWRITE_JPEG_QUALITY, 95])
