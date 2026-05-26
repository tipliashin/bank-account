import re


class EmptyFileError(Exception):
    pass


try:
    with open("input.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        if not lines:
            raise EmptyFileError("Файл пуст, нечего обрабатывать")

        with open("output.txt", "w", encoding="utf-8") as f_o:
            for i, line in enumerate(lines, 1):
                clean_line = line.rstrip("\n")
                numbers = re.findall(r"\d+", line)
                total = sum(int(num) for num in numbers)
                f_o.write(f'Строка {i}: "{clean_line}" -> сумма = {total}\n')

except FileNotFoundError:
    print("Файл input.txt не найден")
except EmptyFileError as e:
    print(e)
