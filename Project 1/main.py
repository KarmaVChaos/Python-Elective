import copy
import math
import random
from operator import concat

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pass

#my code
def ex1():
    while True:
        print("please input two number for sum:")
        a,b = int(input()),int(input()) #Внимание, ввод через энтр дважы, а не в одну строку. Улучшить
        sum = a+b
        print("summary = ",sum)

def ex2():
    end = int(12)
    elem = int(1)
    a = str('')
    while elem < (end*2)+2:
        if elem % 2 == 1:
            a = concat(a,'*\t')
            #print('*\t')
        else:
            a = concat(a,concat(str(elem//2), '\t'))
            #print(elem,'\t')
        if elem % 5 == 0:
            print(a)
            a =''
        elem+=1
    '''Через функцию можно задать аргументы конца и правила вывода. Можно доработать код'''

def ex3():
    print("Загадайте число. Введите граници интервала, в котором оно находится")
    #Примечание: Интервал это (left,right), таким образом, эти числа не могут быть ответом
    right, left = int(input()),int(input())
    if right < left:
        right, left = left, right
    while True:
        N = (right-left) // 2 + left
        print("Число равно {}?".format(N))
        answer = int(input())
        if answer:
            print("good! I found answer")
            break
        elif N>=right or N<=left:
            print("Ты меня где-то обманул!!!!\nИгра окончена!")
            break
        else:
            print("Число меньше {}?".format(N))
            answer = int(input())
            if answer:
                right = N
            else:
                left = N
            #print(left, right)

def ex4():
    print("Поиск максимального числа из введёнх чисел. 0 - число завершения")
    max = 0
    while True:
        a = int(input())
        if a==0:
            break
        elif a<0:
            print("error, number must be positive")
        elif a>max:
            max = a
    print("max = ",max)


def ex5():
    #ЗАДАНИЕ: вывести таблицу множения
    end = int(11)   # число столбцов и их нижняя граница в
    width = int(6)  # количество столбцов в ширину
    begin = int(2)  # первый столбец в таблице
    j = 1           # счётчик длины столбца
    while begin < end:
        line = ""
        for i in range(begin, begin+width, 1):
            if i > end: break
            line = line + "{} x {} = {}\t\t".format(i, j, j * i)
        print(line)

        j += 1
        if j > end:
            begin = begin + width
            j = 1
            print()

def list_ex1():
    length = 11
    min_elem = 1
    max_elem = 20
    a = createRandomArray(length, min_elem, max_elem)
    print('Дана выборка из {} чисел.\n{}'.format(len(a), a))

    a.sort()
    print(a)
    print('Максимум: ', max(a))
    print('Минимум: ', min(a))
    print('Медиана ', a[len(a)//2])

def list_ex2():
    # Гистограммa
    length = 20
    min_elem = 0
    max_elem = 100
    quant = 10
    '''
    Примечание: кванование неравномерное.
    при [0,100] получается всего 101 элемент. диапазоны не равномерные
    '''
    array = createRandomArray(length, min_elem, max_elem)
    print('Дана выборка из {} чисел.\n{}'.format(len(array), array))
    print(sorted(array))
    gist = [0 for i in range((max_elem-min_elem)//quant)]
    #спорное, но рабочее решение
    for value in array:
        if value == max_elem:
            gist[len(gist)-1]+=1
            continue
        gist[value//quant] += 1
    print(gist)

    #преобразование в вероятности

    p = [val/sum(gist) for val in gist]
    print(p)
    print(sum(p))

def list_ex3():
    N = 5 #размерность вектора
    scalar = int(8) #
    vec1 = createRandomArray(N,-5,5)
    vec2 = createRandomArray(N,-5,5)

    # требуется рефакторинг и оптимизация. Должно быть решение лучше
    vec = [vec1[i]+vec2[i] for i in range(len(vec1))]
    '''
    vec = copy.deepcopy(vec1)
    for i in range(len(vec)):
        vec[i] += vec2[i]
    '''
    vecX = [vec1[i] * vec2[i] for i in range(len(vec1))]
    '''
    vecX = copy.deepcopy(vec1)
    for i in range(len(vecX)):
        vecX[i] *= vec2[i]
    '''
    '''
    vecScalar = copy.deepcopy(vec1) if norm(vec1)>norm(vec2) else copy.deepcopy(vec2)
    for val in vecScalar: val*=scalar
    '''
    vecScalar = [val*scalar for val in (copy.deepcopy(vec1) if norm(vec1)>norm(vec2) else copy.deepcopy(vec2))]

    print('покомпонентная сумма', vec)
    print('покомпонентное произведение', vecX)
    print('умножение вектора на скаляр', vecScalar)

def list_ex4():
    #входные данные
    length = 5
    a = [createRandomArray(length,0,10) for i in range(length)]
    b = createRandomArray(length,0,10)

    #умножение матрицы на вектор

    pass

def list_ex5():
    '''
    перечень проблем:
    Нужно ли сохраянть старые значения элементов?
    Как закладывать поведение на случай отсутствия положительных элементов?
        Если положительный всего 1?

    '''
    #входные данные
    '''
    N = int(input())
    a = getConsolVector(N)
    '''
    a = createRandomArray(25, -10,10)

    #Решение
    #Проблема Крайних Элементов!
    if max(a)<0:
        print("Error, not positive number. All elements be corrupted")
        a[0] = 0

    left, right, right_first = -1, -1, -1
    for j in range(len(a)):
        if a[j] >= 0:
            right_first = a[j]
            right = right_first
            break
    for j in range(1, len(a)-1):
        if a[-j] >= 0:
            left = a[-j]
            break

    for i in range(len(a)):
        if a[i]<0:
            a[i] = (left+right)//2
        else:
            left = a[i]
            for j in range(i+1, len(a)):
                if a[j]>=0:
                    right = a[j]
                    break
                if j==len(a)-1:
                    right = right_first
    print(a)

def list_ex6():# СВЁРТКА!
    #входные данные
    arr = createRandomArray(9,1,20)
    mask = createRandomArray(3,-2,2) # [1,-2,1,1]
    '''
    ans = []
    for i in range(len(arr)-len(mask)+1):
        mn = []
        for j in range(len(mask)):
            mn.append(arr[i+j]*mask[j])
        ans.append(sum(mn))
    '''
    ans = [sum([arr[i+j]*mask[j] for j in range(len(mask))]) for i in range(len(arr)-len(mask)+1)]
    print(ans)


#Вспомогательные функции
def createRandomArray(length:int, min_elem:int, max_elem:int):
    a = [random.randint(min_elem, max_elem) for i in range(length)]
    #Контроль
    print('Создан список: ',a)
    return a

def norm(vector:list):
    return int(math.sqrt(sum([value**2 for value in vector])))

def getConsolMatrix(width:int, high:int):
    return [getConsolVector(width) for i in range(0,high)]

def getConsolVector(length:int): #not stable!
    return [int(val) for val in input().split(' ',length)]# input().split()

def printGistogram():
    #как будто лишено смысла...
    pass


#main
def start():
    flag = True
    while flag:
        print("введите номер задания который хотите проверить [0; 11]. 0 - Завершить работу программы")
        answer = int(input())
        match answer:
            case 0:
                flag = False
            #задачи 1-5 по циклам
            case 1:
                ex1()
            case 2:
                ex2()
            case 3:
                ex3()
            case 4:
                ex4()
            case 5:
                ex5()
            # задачи 1-6 по спискам
            case 6:
                list_ex1()
            case 7:
                list_ex2()
            case 8:
                list_ex3()
            case 9:
                list_ex4()
            case 10:
                list_ex5()
            case 11:
                list_ex6()
    else: print('Конец программы')


#executable code
start()


''' Задачи:
    циклы
    1) - готово
    2) - готово
    3) - готово
    4) - готово
    5) - готово
    списки
    1) - готово
    2) - готово
    3) - готово
    4) - уточнить задание
    5) - готово, не оптимально, проблема крайних элементов
    6) - готово
'''