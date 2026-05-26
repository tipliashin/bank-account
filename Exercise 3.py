n = int(input("Введите N: "))
if n < 2:
    print("Простых чисел в этом диапазоне нет.")
else:
    for i in range(2, n):
        for x in range(2, i):
            if i % x == 0:
                break
        else:
            print(i)
