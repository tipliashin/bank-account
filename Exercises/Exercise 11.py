from collections import deque

d = deque([1, 2, 3])
d.append(4)  # добавили в конец
d.appendleft(0)  # добавили в начало
print(d)  # deque([0, 1, 2, 3, 4])
print(d.pop())  # убрали с конца → 4
print(d.popleft())  # убрали с начала → 0

tasks = deque()
tasks.append("задача 1")
tasks.append("задача 2")
tasks.append("задача 3")

while tasks:
    current = tasks.popleft()
    print(f"Выполняем: {current}")


def is_valid(s: str) -> bool:
    stack = []
    is_valid_bool = False
    pairs = {')': '(', ']': '[', '}': '{'}
    for char in s:
        if char in "([{":
            stack.append(char)
        if (char in ")}]") and stack:
            last = stack.pop()
            if (last == "(" and char == ")") or (last == "[" and char == "]") or (last == "{" and char == "}"):
                is_valid_bool = True
            else:
                is_valid_bool = False
                break
        elif not stack:
            is_valid_bool = False
            break
    if stack:
        is_valid_bool = False
    return is_valid_bool


print(is_valid(""))        # True (пустая строка считается валидной)
print(is_valid("("))       # False
print(is_valid(")"))       # False
print(is_valid("(([]){})")) # True

def is_valid(s: str) -> bool:
    """
    Проверяет, является ли скобочная последовательность правильной.
    """
    # Словарь для быстрого поиска пары
    pairs = {')': '(', ']': '[', '}': '{'}
    stack = []

    for char in s:
        # Если это открывающая скобка — кладём в стек
        if char in pairs.values():  # '(', '[', '{'
            stack.append(char)
        # Если это закрывающая скобка
        elif char in pairs:         # ')', ']', '}'
            # Если стек пуст или вершина не соответствует — ошибка
            if not stack or stack.pop() != pairs[char]:
                return False
        # Неизвестные символы игнорируем (по условию их нет)

    # В конце стек должен быть пуст (все открывающие скобки закрыты)
    return not stack


# Тесты
test_cases = [
    ("()", True),
    ("()[]{}", True),
    ("(]", False),
    ("([)]", False),
    ("{[]}", True),
    ("", True),
    ("(", False),]

for s, expected in test_cases:
    result = is_valid(s)
    status = "✓" if result == expected else "✗"
    print(f'{status} is_valid("{s}") = {result} (expected {expected})')