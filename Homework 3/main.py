import random

# ================== ЗАДАНИЕ 1 ==================
def table(func, begin = 1, end = 9, width = 5):
    # решение не является оптимальным, но работает
    #begin =  первый столбец в таблице
    #end =  число столбцов и их нижняя граница в
    #width = количество столбцов в ширину
    j = 1  # счётчик длины столбца
    operator = {
        '*': multiplication,
        '/': division,
        '+': addition,
        '-': subtraction
    }

    while begin <= end:
        line = ""
        for i in range(begin, begin + width, 1):
            if i > end: break
            line = line + "{} {} {} = {}\t\t".format(i, func, j, operator[func](i,j))
        print(line)

        j += 1
        if j > end:
            begin = begin + width
            j = 1
            print()

def multiplication(arg, inter):
    return arg * inter

def division(arg, inter):
    return arg / inter

def addition(arg, inter):
    return arg + inter

def subtraction(arg, inter):
    return arg - inter


def tablesPrint():
    # эта функция является интерфейсом для пользователя
    print("Доступные операции: + - * /")
    print("Примеры шаблонов (аргументы : пример ввода)")
    print("op                   :+")
    print("op width             :- 5")
    print("begin op end         :1 * 9")
    print("begin op end width   :2 / 9 4")

    argLine = input("Ваша таблица или шаблон: ").split()
    print(argLine)
    if len(argLine) == 1:
        table(argLine[0])
    elif len(argLine) == 2:
        table(argLine[0], width=int(argLine[1]))
    elif len(argLine) == 3:
        table(argLine[1], begin=int(argLine[0]), end=int(argLine[2]))
    elif len(argLine) == 4:
        table(argLine[1], begin=int(argLine[0]), end=int(argLine[2]), width=int(argLine[3]))
    else:
        print("ошибка ввода шаблона")


# ================== ЗАДАНИЕ 2 ==================
def create_vector(N):
    return [random.random() for _ in range(N)]


def create_matrix(M, N):
    return [create_vector(N) for _ in range(M)]


def matrix_vector_multiply(matrix, vector):
    result = []
    for row in matrix:
        if len(row) != len(vector):
            print("Несовместимые размеры")
            return
        result.append(sum(row[j] * vector[j] for j in range(len(vector))))
    return result


def print_matrix(matrix):
    for vector in matrix:
        print_vector(vector)


def print_vector(vector):
    print(' '.join(f'{x}' for x in vector))


def diagonal_sum(matrix):
    return sum(matrix[i][i] for i in range(len(matrix)))


def convolution2d(image, kernel):
    img_h, img_w = len(image), len(image[0])
    ker_h, ker_w = len(kernel), len(kernel[0])
    result = []

    for i in range(img_h - ker_h + 1):
        row = []
        for j in range(img_w - ker_w + 1):
            val = 0
            for ki in range(ker_h):
                for kj in range(ker_w):
                    val += image[i + ki][j + kj] * kernel[ki][kj]
            row.append(val)
        result.append(row)
    return result


# ================== ЗАДАНИЕ 3 ==================
def multichannel_wrapper(conv_func):
    def wrapper(image, kernel):
        channels = []
        for channel in range(3):
            single_channel = [[pixel[channel] for pixel in row] for row in image]
            filtered_channel = conv_func(single_channel, kernel)
            channels.append(filtered_channel)

        result = []
        for i in range(len(channels[0])):
            row = []
            for j in range(len(channels[0][0])):
                pixel = [channels[c][i][j] for c in range(3)]
                row.append(pixel)
            result.append(row)
        return result

    return wrapper


@multichannel_wrapper
def multichannel_convolution(image, kernel):
    return convolution2d(image, kernel)


# ================== ЗАДАНИЕ 4 ==================
def color_conversion(color_vector):
    if len(color_vector) != 4:
        print("Вектор должен содержать 4 компонента")

    if color_vector[3] == 0:  # RGB to YIQ
        R, G, B = color_vector[:3]
        Y = 0.299 * R + 0.587 * G + 0.114 * B
        I = 0.596 * R - 0.274 * G - 0.322 * B
        Q = 0.211 * R - 0.523 * G + 0.312 * B
        return [Y, I, Q, 1]

    elif color_vector[3] == 1:  # YIQ to RGB
        Y, I, Q = color_vector[:3]
        R = Y + 0.956 * I + 0.621 * Q
        G = Y - 0.272 * I - 0.647 * Q
        B = Y - 1.106 * I + 1.703 * Q
        return [R, G, B, 0]

    else:
        print("Неверный тип цветовой модели")


# ================== ОСНОВНАЯ ПРОГРАММА ==================
def main():
    flag = True
    while flag:
        print("\nВыберите задание:")
        print("1 : Таблицы умножения/деления/сложения/вычитания")
        print("2 : Матрицы")
        print("3 : Многоканальная свертка")
        print("4 : конвертация цветов")
        print("0 : Выход")

        choice = input("Введите номер: ")

        if choice == '1':
            tablesPrint()
        elif choice == '2':
            # Демонстрация работы с матрицами
            v = create_vector(3)
            m = create_matrix(3, 3)
            print("Вектор:")
            print_vector(v)
            print("Матрица:")
            print_matrix(m)
            print("Умножение матрицы на вектор:")
            print_vector(matrix_vector_multiply(m, v))
            print("Сумма диагонали:", diagonal_sum(m))
        elif choice == '3':
            # Пример многоканальной свертки
            image = [[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                     [[9, 8, 7], [6, 5, 4], [3, 2, 1]],
                     [[1, 3, 5], [7, 9, 2], [4, 6, 8]]]
            kernel = [[0.1, 0.2], [0.3, 0.4]]
            result = multichannel_convolution(image, kernel)
            print("Результат свертки:")
            for row in result:
                print(row)
        elif choice == '4':
            # Пример конвертации цветов
            rgb = [0.5, 0.3, 0.8, 0]
            yiq = color_conversion(rgb)
            back_to_rgb = color_conversion(yiq)
            print(f"RGB: {rgb[:3]} -> YIQ: {yiq[:3]} -> RGB: {back_to_rgb[:3]}")
        else:
            pass


if __name__ == '__main__':
    main()

