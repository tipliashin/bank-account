# def countdown(n):
#     while n > 1:
#         yield n
#         n -= 1
#
# for num in countdown(5):
#     print(num)
#
# squares = (x ** 2 for x in range(1,10))  # генератор
# print(next(squares))  # 0
# print(next(squares))
# print(next(squares))
# print(next(squares))
# print(next(squares))
# print(next(squares))


def fibonacci(n):
    a, b = 1, 1
    for _ in range(n):
        yield a
        a, b = b, a + b
    # x = 1
    # y = 0
    # while n > 0:
    #     yield x
    #     z = y
    #     y = x
    #     x += z
    #     n -= 1


def read_lines_with_filter(filename, keyword):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                if keyword in line:
                    yield line
    except FileNotFoundError:
        # print(f"Файл {filename} не найден")
        return


for num in fibonacci(15):
    print(num)

with open("../test_log.txt", "w", encoding="utf-8") as f_w:
    f_w.write("INFO: Запуск\nERROR: Сбой\nDEBUG: Проверка\nERROR: Ошибка\n")

for line in read_lines_with_filter("../test_log.txt", "ERROR"):
    print(line, end="")
