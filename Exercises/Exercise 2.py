a, b, c = map(int, input("Введите три числа: ").split())
print(a, b, c)
sum_of_ab = (
    "Сумма первых двух больше" if (b + a) > c else "Третье больше или равно сумме"
)
if a >= b and a >= c:
    print(f"Максимальное: {a}")
elif b >= a and b >= c:
    print(f"Максимальное: {b}")
else:
    print(f"Максимальное: {c}")
if a > 0 and b > 0 and c > 0:
    print("Все положительные")
else:
    print("Не все положительные")
print(sum_of_ab)
