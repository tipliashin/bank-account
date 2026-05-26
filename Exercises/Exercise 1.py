from datetime import date

"""

name = input("Enter your name")
age = input("Enter your age")
try:
    dateborn = date.today().year - int(age)
    print(f"Привет, {name}! Ты родился примерно в {dateborn} году.")
except:
    dateborn = 0
    print("Введите возраст числом")
"""

name = input("Введите имя: ")
age_input = input("Введите возраст: ")

try:
    age = int(age_input)
except ValueError:
    age = 0
    print("Возраст введён некорректно, будет использован 0.")

birth_year = date.today().year - age
print(f"Привет, {name}! Ты родился примерно в {birth_year} году.")
