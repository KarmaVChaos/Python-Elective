import re

_RU = {
    'size': [r'размер\s+изображения\s+(\d+)\s*[xXхХ×]\s*(\d+)'],
    'count': [r'количество\s+(?:объектов|клеток)\s+(?:равно\s+)?(\d+)'],
    'gray': [r'оттенк\w\s+серого', r'чёрно.?бел'],
    'overlap': [r'пересечени[ея]\s+(?:объектов\s+)?(?:разрешен|допустим)']
}
_EN = {
    'size': [r'image\s+size\s+(\d+)\s*[xX×]\s*(\d+)'],
    'count': [r'number\s+of\s+(?:objects?|cells?)\s+(?:is\s+)?(\d+)'],
    'gray': [r'gr[ae]yscale', r'black\s+and\s+white'],
    'overlap': [r'overlap\s+(?:is\s+)?(?:allowed|permitted)']
}

def parse_params(text: str, lang: str = 'en') -> dict:
    p = _EN if lang == 'en' else _RU
    t = text.lower()
    result = {'color_mode': 'RGB', 'allow_overlap': False}
    for pat in p['size']:
        m = re.search(pat, t)
        if m: result['image_size'] = [int(m.group(1)), int(m.group(2))]; break
    for pat in p['count']:
        m = re.search(pat, t)
        if m: result['num_objects'] = int(m.group(1)); break
    for pat in p['gray']:
        if re.search(pat, t): result['color_mode'] = 'grayscale'; break
    for pat in p['overlap']:
        if re.search(pat, t): result['allow_overlap'] = True; break
    return result