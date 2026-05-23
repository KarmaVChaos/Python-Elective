import random

def generate_description(image_size, num_cells, grayscale=False, allow_overlap=True, lang='en'):
    w, h = image_size
    if lang == 'ru':
        color = 'в оттенках серого' if grayscale else 'цветное RGB'
        overlap = 'разрешено' if allow_overlap else 'запрещено'
        return f'Конфигурация: размер {w}x{h}, количество клеток {num_cells}, режим {color}, пересечение {overlap}.'
    color = 'grayscale' if grayscale else 'RGB color'
    overlap = 'allowed' if allow_overlap else 'not allowed'
    return f'Image generator config: size {w}x{h}, {num_cells} cells, {color}, overlap {overlap}.'