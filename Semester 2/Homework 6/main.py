from text_processor.morse_codec import encode_text, decode_text, check_is_morse
from text_processor.morse_detect import MorseKNN
from text_processor.lang_detect import LangKNN
from text_processor.params import parse_params
from text_reader import TextReader
from discription_gen import generate_description

def run_tests():
    print("=== Morse Codec ===")
    original = 'IMAGE SIZE 256'
    enc = encode_text(original, 'en')
    print(f"Original: {original}\nEncoded : {enc}\nDecoded : {decode_text(enc, 'en')}\nIs Morse: {check_is_morse(enc)}\n")

    print("=== Morse Detector ===")
    mknn = MorseKNN()
    for t, exp in [('... ..', True), ('image size', False)]:
        print(f'"{t}" -> morse={mknn.predict(t)} (expected={exp})')
    print()

    print("=== Language Detector ===")
    lknn = LangKNN()
    for t, exp in [('размер изображения', 'ru'), ('image size 256', 'en')]:
        print(f'"{t}" -> lang={lknn.predict(t)} (expected={exp})')
    print()

    print("=== Parameter Parser ===")
    print(f"EN: {parse_params('image size 128x128. number of cells 3.', 'en')}")
    print(f"RU: {parse_params('размер изображения 256x256. количество клеток 5.', 'ru')}\n")

    print("=== Text Reader (Files) ===")
    reader = TextReader()
    for f in ['data/sample_en.txt', 'data/sample_ru.txt', 'data/sample_morse_en.txt']:
        res = reader.read_file(f)
        print(f"{f}:\n  lang={res['_lang']}, morse={res['_was_morse']}\n  params={ {k:v for k,v in res.items() if not k.startswith('_')} }\n")

    print("=== Description Generator ===")
    print(generate_description([256, 256], 5, grayscale=False, allow_overlap=True, lang='en'))
    print(generate_description([128, 128], 3, grayscale=True, allow_overlap=False, lang='ru'))

if __name__ == '__main__':
    run_tests()