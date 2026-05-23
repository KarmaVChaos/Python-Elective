from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier

class LangKNN:
    def __init__(self, k=3):
        self.k = k
        self._vec = TfidfVectorizer(analyzer='char', ngram_range=(3, 5), max_features=200)
        self._clf = KNeighborsClassifier(n_neighbors=k)
        ru = ['размер изображения количество клеток', 'конфигурация генератора']
        en = ['image size number of cells', 'generator configuration overlap']
        self.fit(ru + en, ['ru'] * len(ru) + ['en'] * len(en))

    def fit(self, texts, labels):
        X = self._vec.fit_transform(texts)
        self._clf.fit(X, labels)

    def predict(self, text):
        if any('Ѐ' <= c <= 'ӿ' for c in text): return 'ru'
        if text.isascii(): return 'en'
        return self._clf.predict(self._vec.transform([text]))[0]