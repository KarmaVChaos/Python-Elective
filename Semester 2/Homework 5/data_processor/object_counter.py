import cv2
import numpy as np
from .processor_plugin import DataProcessorMeta


class ObjectCounter(DataProcessorMeta, processor_name='count'):
    def process(self, image: np.ndarray) -> dict:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image.copy()

        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        cleaned = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

        n_labels, labels, stats, _ = cv2.connectedComponentsWithStats(cleaned, connectivity=8)

        min_area = 50
        bboxes = []
        for i in range(1, n_labels):
            area = stats[i, cv2.CC_STAT_AREA]
            if area >= min_area:
                x = int(stats[i, cv2.CC_STAT_LEFT])
                y = int(stats[i, cv2.CC_STAT_TOP])
                w = int(stats[i, cv2.CC_STAT_WIDTH])
                h = int(stats[i, cv2.CC_STAT_HEIGHT])
                bboxes.append((x, y, w, h))

        return {'num_objects': len(bboxes), 'bboxes': bboxes}
