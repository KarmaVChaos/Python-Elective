import numpy as np
import cv2
from .processor_plugin import DataProcessorMeta


class KNNProcessor(DataProcessorMeta, processor_name='knn'):
    def __init__(self, k: int = 3):
        self.k = k
        self._train_features: list = []
        self._train_labels: list = []

    def fit(self, images: list, labels: list) -> None:
        self._train_features = [self._extract_features(img) for img in images]
        self._train_labels = list(labels)

    def process(self, image: np.ndarray) -> dict:
        if not self._train_features:
            return {'label': None, 'distances': [], 'message': 'Model not fitted yet'}

        query = self._extract_features(image)
        distances = [self._l2(query, f) for f in self._train_features]
        k_idx = np.argsort(distances)[:self.k]
        k_labels = [self._train_labels[i] for i in k_idx]
        k_dists = [float(distances[i]) for i in k_idx]

        label = max(set(k_labels), key=k_labels.count)
        return {'label': label, 'k_neighbors': k_labels, 'distances': k_dists}

    def _extract_features(self, image: np.ndarray) -> np.ndarray:
        img = cv2.resize(image, (64, 64))
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) if len(img.shape) == 3 else img
        hist_h = cv2.calcHist([hsv], [0], None, [16], [0, 180]).flatten()
        hist_s = cv2.calcHist([hsv], [1], None, [16], [0, 256]).flatten() if len(img.shape) == 3 else np.zeros(16)
        hist_v = cv2.calcHist([hsv], [2] if len(img.shape) == 3 else [0], None, [16], [0, 256]).flatten()
        feat = np.concatenate([hist_h, hist_s, hist_v])
        norm = np.linalg.norm(feat)
        return feat / norm if norm > 0 else feat

    @staticmethod
    def _l2(a: np.ndarray, b: np.ndarray) -> float:
        return float(np.linalg.norm(a - b))
