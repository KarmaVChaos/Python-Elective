import numpy as np
from .morse_codec import check_is_morse

class MorseKNN:
    def __init__(self, k=3):
        self.k = k
        self._train_x = []
        self._train_y = []
        plain = ['image size 256x256 number of cells 5 rgb', 'размер изображения 256x256']
        morse = ['... .. --.. . / ..- ... -... / -.-. . .-.. .-.. ... / ...', '.. -- .- --. . / ... .. --.. . / ..- ... -...']
        self.fit(plain + morse, [False, False, True, True])

    def fit(self, texts, labels):
        self._train_x = [self._features(t) for t in texts]
        self._train_y = list(labels)

    def predict(self, text):
        if check_is_morse(text):
            return True
        q = self._features(text)
        dists = [float(np.linalg.norm(q - f)) for f in self._train_x]
        top_k = sorted(range(len(dists)), key=lambda i: dists[i])[:self.k]
        return sum(self._train_y[i] for i in top_k) > len(self._train_y) / 2

    def _features(self, text):
        n = max(len(text), 1)
        return np.array([
            text.count('.') / n,
            text.count('-') / n,
            text.count('/') / n,
            sum(c.isalpha() for c in text) / n,
            sum(c.isdigit() for c in text) / n
        ], dtype=np.float32)