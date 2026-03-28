import json
import os
import re
from typing import List, Union


class MorseExtendedConverter:
    """
    Загружает из JSON все коды: буквы, цифры, операции.
    Предоставляет методы для преобразования символ -> морзе и морзе -> символ.
    """
    def __init__(self, file_path: str):
        self._sym_to_morse = {}
        self._morse_to_sym = {}
        self._load_table(file_path)

    def _load_table(self, file_path: str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} not found")
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # Объединяем все разделы в один словарь
        for section in ('morse_eng', 'morse_digits', 'morse_ops'):
            if section in data:
                self._sym_to_morse.update(data[section])
        # Построить обратный словарь
        self._morse_to_sym = {v: k for k, v in self._sym_to_morse.items()}

    def to_morse(self, symbol: str) -> str:
        """Вернуть морзе-код символа."""
        return self._sym_to_morse[symbol]

    def from_morse(self, code: str) -> str:
        """Вернуть символ по морзе-коду."""
        return self._morse_to_sym[code]

    def is_valid_symbol(self, symbol: str) -> bool:
        return symbol in self._sym_to_morse

    def is_valid_morse(self, code: str) -> bool:
        return code in self._morse_to_sym

    def __getitem__(self, key):
        return self.to_morse(key)

    def __call__(self, key):
        return self.to_morse(key)

    def __len__(self):
        return len(self._sym_to_morse)

    def __iter__(self):
        return iter(self._sym_to_morse.values())


class TextToMorseConverter:
    """
    Конвертирует обычные текстовые строки (буквы, цифры, операторы) в морзе-строку.
    Правила:
      - между каждым символом (буквой, цифрой, оператором) – один пробел
      - между словами / числами / операторами – три пробела
      - внутри чисел пробелы между разрядами также один пробел
    """
    def __init__(self, converter: MorseExtendedConverter):
        self._converter = converter

    def text_to_morse(self, text: str) -> str:
        """
        Преобразует обычную строку (буквы, цифры, операторы) в строку морзе.
        """
        # Разбиваем строку на слова (последовательности символов, разделённые пробелами)
        words = text.split()
        morse_parts = []
        for word in words:
            # Каждый символ слова конвертируем в морзе и объединяем через пробел
            morse_word = ' '.join(self._converter.to_morse(ch) for ch in word)
            morse_parts.append(morse_word)
        # Между словами – три пробела
        return '   '.join(morse_parts)

    def morse_to_text(self, morse_str: str) -> str:
        """
        Преобразует строку морзе (с правилами: символы разделены пробелом, слова – тремя пробелами)
        в обычный текст.
        """
        words = morse_str.split('   ')   # разделяем по трём пробелам
        result_words = []
        for word in words:
            if not word:
                continue
            chars = word.split()
            text_word = ''.join(self._converter.from_morse(ch) for ch in chars)
            result_words.append(text_word)
        return ' '.join(result_words)


class MorseNumber:
    """
    Представляет целое число, которое можно использовать в арифметических
    операциях и сравнениях. Внутренне хранит int, а для ввода/вывода
    использует конвертер.
    """
    _converter = None   # общий для всех экземпляров конвертер

    @classmethod
    def set_converter(cls, converter: MorseExtendedConverter):
        cls._converter = converter

    def __init__(self, value: Union[int, str]):
        if MorseNumber._converter is None:
            raise RuntimeError("MorseNumber: конвертер не установлен")
        if isinstance(value, int):
            self._value = value
        elif isinstance(value, str):
            # Строка морзе: цифры разделены пробелами (каждая цифра – один морзе-код)
            parts = value.split()
            digits = []
            for part in parts:
                if not MorseNumber._converter.is_valid_morse(part):
                    raise ValueError(f"Неверный морзе-код цифры: {part}")
                sym = MorseNumber._converter.from_morse(part)
                if not sym.isdigit():
                    raise ValueError(f"Символ {sym} не является цифрой")
                digits.append(sym)
            self._value = int(''.join(digits))
        else:
            raise TypeError("value должен быть int или str")

    def __int__(self):
        return self._value

    def __str__(self):
        """Возвращает строку морзе (цифры разделены пробелами)."""
        digits = str(self._value)
        codes = [MorseNumber._converter.to_morse(d) for d in digits]
        return ' '.join(codes)

    def __repr__(self):
        return f"MorseNumber({self._value})"

    # Арифметические операции
    def __add__(self, other):
        if not isinstance(other, MorseNumber):
            other = MorseNumber(other)
        return MorseNumber(self._value + other._value)

    def __sub__(self, other):
        if not isinstance(other, MorseNumber):
            other = MorseNumber(other)
        return MorseNumber(self._value - other._value)

    def __mul__(self, other):
        if not isinstance(other, MorseNumber):
            other = MorseNumber(other)
        return MorseNumber(self._value * other._value)

    def __truediv__(self, other):
        if not isinstance(other, MorseNumber):
            other = MorseNumber(other)
        if other._value == 0:
            raise ZeroDivisionError("Деление на ноль")
        # Целочисленное деление
        return MorseNumber(self._value // other._value)

    def __floordiv__(self, other):
        return self.__truediv__(other)

    # Сравнения
    def __eq__(self, other):
        if not isinstance(other, MorseNumber):
            other = MorseNumber(other)
        return self._value == other._value

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if not isinstance(other, MorseNumber):
            other = MorseNumber(other)
        return self._value < other._value

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        return not (self <= other)

    def __ge__(self, other):
        return not (self < other)

    def __neg__(self):
        return MorseNumber(-self._value)

    def __abs__(self):
        return MorseNumber(abs(self._value))


class MorseCalculator:
    """
    Обрабатывает строки разных типов:
      - если строка содержит буквы -> просто преобразует в морзе (текстовый режим)
      - иначе, если есть '=', вычисляет выражения и возвращает результат
      - иначе (только цифры и операторы, без '=') -> преобразует в морзе
    """
    def __init__(self, converter: MorseExtendedConverter):
        self._converter = converter
        self._text_converter = TextToMorseConverter(converter)

    def _evaluate_expression(self, expr_str: str) -> int:
        """
        Вычисляет арифметическое выражение, заданное строкой с пробелами.
        Поддерживает + - * / и целые числа.
        """
        # Удаляем пробелы, оставляем только цифры и операторы
        clean_expr = ''.join(expr_str.split())
        # Проверяем допустимые символы
        if not re.fullmatch(r'[\d+\-*/]+', clean_expr):
            raise ValueError(f"Недопустимое выражение: {expr_str}")
        # Безопасное вычисление
        return eval(clean_expr, {"__builtins__": None}, {})

    def _number_to_result(self, num: int) -> str:
        """Преобразует число в формат: морзе (арабское)"""
        morse_num = MorseNumber(num)
        return f"{morse_num} ({num})"

    def process(self, text: str) -> str:
        """Основной метод обработки строки."""
        # Категория 1: есть буквы -> просто преобразовать в морзе
        if any(ch.isalpha() for ch in text):
            return self._text_converter.text_to_morse(text)

        # Категория 2:
        # Разделяем по '=' и чистим для вычислений
        parts = text.split('=')
        parts = [p.strip() for p in parts]

        # Если нет '=' (одна часть)
        if len(parts) == 1:
            return self._text_converter.text_to_morse(parts[0])

        # Обработка нескольких '='
        result_parts = []
        # Для всех частей, кроме последней, вычисляем выражение
        for i in range(len(parts) - 1):
            expr = parts[i]
            if expr == '':
                # Пустая левая часть (например, "= 5") – игнорируем
                continue
            try:
                value = self._evaluate_expression(expr)
                result_parts.append(self._number_to_result(value))
            except Exception as e:
                # Если выражение некорректно, на всякий случай:
                result_parts.append(self._text_converter.text_to_morse(expr))

        # Последнюю часть (если не пустая) просто преобразуем в морзе
        last = parts[-1]
        if last:
            result_parts.append(self._text_converter.text_to_morse(last))

        return '   '.join(result_parts)


def run_tests(calculator: MorseCalculator):
    """
    Набор тестов для трёх категорий:
      1. Текстовые строки (только буквы)
      2. Смешанные строки (буквы + цифры/операторы) – обрабатываются как текст
      3. Арифметические выражения (только цифры и операторы)
    """
    tests = [
        # Категория 1: только буквы
        ("hello world", ".... . .-.. .-.. ---   .-- --- .-. .-.. -.."),
        ("mipt", "-- .. .--. -"),
        # Категория 2: смешанные (с буквами) – просто конвертация
        ("abc 123", ".- -... -.-.   .---- ..--- ...--"),
        ("mipt 2026", "-- .. .--. -   ..--- ----- ..--- -...."),
        # Категория 3: выражения без '=' – просто конвертация
        ("2 + 3", "..---   .-.-.   ...--"),
        ("20 * 3", "..--- -----   -..-   ...--"),
        # Категория 3: выражения с одним '='
        ("4 + 3 = ", "--... (7)"),
        ("2 + 3 * 4 = ", ".---- ....- (14)"),
        # Категория 3: выражения с двумя '='
        ("2 + 2 = 3 + 3 = 5 + 5", "....- (4)   -.... (6)   .....   .-.-.   ....."),
        ("= 10 + 10", ".---- -----   .-.-.   .---- -----"),  # пустая левая часть игнорируется
    ]

    print("Запуск тестов:\n")
    for i, (input_text, expected) in enumerate(tests, 1):
        result = calculator.process(input_text)
        status = "✓" if result == expected else "✗"
        print(f"Тест {i}: {status}")
        print(f"  Вход:   {input_text}")
        print(f"  Ожидалось: {expected}")
        print(f"  Получено:  {result}")
        print()

def main():
    # Загружаем конвертер
    converter = MorseExtendedConverter('morse.json')
    # Устанавливаем конвертер для MorseNumber
    MorseNumber.set_converter(converter)

    # Создаём калькулятор
    calculator = MorseCalculator(converter)

    # Запускаем тесты
    run_tests(calculator)

if __name__ == "__main__":
    main()