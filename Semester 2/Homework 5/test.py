import importlib
import pkgutil

import data_loader
import data_processor
import data_exporter


_discovered: dict[str, bool] = {}


def autodiscover(package) -> None:
    name = package.__name__
    if _discovered.get(name):
        return
    for m in pkgutil.iter_modules(package.__path__):
        if not m.name.startswith('_'):
            importlib.import_module(f'{name}.{m.name}')
    _discovered[name] = True


def demo_descriptors():
    from descriptors import ValidatedImage, NotEmptyFile, ColorCountValidator, AutoResizeImage
    import numpy as np

    print('\n=== Task 1: Descriptors ===')

    vi = ValidatedImage()
    img = vi.load('./data/COVID-1.png')
    print(f'  ValidatedImage.load  → shape={img.shape}  (expected 256×256×3)')

    class Holder:
        data = AutoResizeImage()

    h = Holder()
    big = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
    h.data = big
    print(f'  AutoResizeImage      → {big.shape} → {h.data.shape}')

    class CV:
        img = ColorCountValidator()

    cv_obj = CV()
    binary = np.zeros((100, 100, 3), dtype=np.uint8)
    binary[:50] = 255
    try:
        cv_obj.img = binary
        print('  ColorCountValidator  → no error (unexpected)')
    except ValueError as e:
        print(f'  ColorCountValidator  → raised ValueError: {e}')


def demo_loaders():
    from data_loader.loader_plugin import DataLoaderMeta

    autodiscover(data_loader)
    print('\n=== Task 2a: Loaders ===')
    print(f'  Registered: {list(DataLoaderMeta._registry.keys())}')

    png = DataLoaderMeta.get_plugin('png')
    img = png.load('./data/COVID-1.png')
    print(f'  PNG  → shape={img.shape}')

    json_loader = DataLoaderMeta.get_plugin('json')
    synthetic = json_loader.load('./data/config.json')
    print(f'  JSON → synthetic image shape={synthetic.shape}')


def demo_processors():
    from data_loader.loader_plugin import DataLoaderMeta
    from data_processor.processor_plugin import DataProcessorMeta
    import numpy as np

    autodiscover(data_loader)
    autodiscover(data_processor)
    print('\n=== Task 2b: Processors ===')
    print(f'  Registered: {list(DataProcessorMeta._registry.keys())}')

    img = DataLoaderMeta.get_plugin('png').load('./data/COVID-1.png')

    counter = DataProcessorMeta.get_plugin('count')
    result = counter.process(img)
    print(f'  ObjectCounter → {result["num_objects"]} object(s) found')

    knn = DataProcessorMeta.get_plugin('knn')
    knn.fit([img, img], ['covid', 'covid'])
    pred = knn.process(img)
    print(f'  KNNProcessor  → predicted label: "{pred["label"]}"')


def demo_exporters():
    from data_loader.loader_plugin import DataLoaderMeta
    from data_exporter.exporter_plugin import DataExporterMeta

    autodiscover(data_loader)
    autodiscover(data_exporter)
    print('\n=== Task 2c: Exporters ===')
    print(f'  Registered: {list(DataExporterMeta._registry.keys())}')

    img = DataLoaderMeta.get_plugin('png').load('./data/COVID-1.png')

    for fmt in ('png', 'jpg', 'bmp', 'json'):
        exp = DataExporterMeta.get_plugin(fmt)
        ok = exp.export(img, f'./data/output.{fmt}')
        print(f'  {fmt.upper()} exporter → {"ok" if ok else "failed"}')


if __name__ == '__main__':
    demo_descriptors()
    demo_loaders()
    demo_processors()
    demo_exporters()
    print('\nAll demos completed.')
