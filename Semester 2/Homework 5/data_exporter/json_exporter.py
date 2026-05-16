import json
import numpy as np
from .exporter_plugin import DataExporterMeta


class JSONExporter(DataExporterMeta, format_name='json'):
    def export(self, image: np.ndarray, filename: str) -> bool:
        path = filename if filename.lower().endswith('.json') else filename + '.json'
        channels = image.shape[2] if len(image.shape) == 3 else 1
        img_3d = image if len(image.shape) == 3 else image[:, :, np.newaxis]

        stats = {
            'shape': list(image.shape),
            'dtype': str(image.dtype),
            'channels': channels,
            'per_channel': [
                {
                    'channel': i,
                    'mean': float(img_3d[:, :, i].mean()),
                    'std': float(img_3d[:, :, i].std()),
                    'min': int(img_3d[:, :, i].min()),
                    'max': int(img_3d[:, :, i].max()),
                }
                for i in range(channels)
            ],
        }
        with open(path, 'w') as f:
            json.dump(stats, f, indent=2)
        return True
