import time
import json


def matrix_matrix_multiply(matrix_a, matrix_b):
    m = len(matrix_a)
    n = len(matrix_a[0]) if m > 0 else 0
    k = len(matrix_b[0]) if len(matrix_b) > 0 else 0

    result = [[0] * k for _ in range(m)]

    for i in range(m):
        for j in range(k):
            for p in range(n):
                result[i][j] += matrix_a[i][p] * matrix_b[p][j]
    return result


def matrix_vector_multiply(matrix, vector):
    m = len(matrix)
    n = len(matrix[0]) if m > 0 else 0

    if n != len(vector):
        print("Ошибка! кол-во столбцов матрицы должно быть равно длине вектора!")
        return None

    result = [0] * m

    for i in range(m):
        for j in range(n):
            result[i] += matrix[i][j] * vector[j]

    return result


def matrix_trace(matrix):
    m = len(matrix)
    n = len(matrix[0]) if m > 0 else 0

    if m != n:
        print("Ошибка! матрица должна быть квадратной!")
        return None

    trace = 0
    for i in range(m):
        trace += matrix[i][i]

    return trace


def vector_vector_scalar_multiply(vector_a, vector_b):
    if len(vector_a) != len(vector_b):
        print("Ошибка! векторы должны быть одинаковой размерности!")
        return None

    result = 0
    for i in range(len(vector_a)):
        result += vector_a[i] * vector_b[i]

    return result


def gistogram(vector, num_bins):
    if num_bins <= 0:
        print("Ошибка! кол-во бинов должно быть положительным")
        return None

    min_val = min(vector)
    max_val = max(vector)
    if min_val == max_val:
        return [len(vector)] + [0] * (num_bins - 1)

    bin_width = (max_val - min_val) / num_bins
    histogram_result = [0] * num_bins

    for value in vector:
        bin_index = int((value - min_val) / bin_width)
        if bin_index >= num_bins:
            bin_index = num_bins - 1
        histogram_result[bin_index] += 1

    return histogram_result


def vector_filter(vector, filter):
    n = len(vector)
    k = len(filter)

    result = []

    for i in range(n - k + 1):
        acc = 0
        for j in range(k):
            acc += vector[i + j] * filter[j]
        result.append(acc)

    return result


def write_to_file(filename, data):
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Данные записаны в файл: {filename}")
        return True
    except Exception as e:
        print(f"Ошибка! {e}")
        return False


def read_from_file(filename):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        print(f"Данные прочитаны из файла: {filename}")
        return data
    except Exception as e:
        print(f"Ошибка! {e}")
        return None


def measure_time(func, *argv):
    start_time = time.time()
    result = func(*argv)
    end_time = time.time()
    elapsed_time = end_time - start_time

    return result, elapsed_time

