from collections import deque

def is_palindrome_deque(s: str) -> bool:
    string = s.lower().replace(" ", "")
    d = deque(string)
    while len(d) > 1:
        if d.popleft() != d.pop():
            return False
    return True


test_cases = [
    ("A man a plan a canal Panama", True),
    ("race a car", False),
    ("aa", True),
    ("aba", True),
    ("", True),          # пустая строка — палиндром
    ("  ", True),        # после очистки — пустая строка
    ("a", True),
]

for s, expected in test_cases:
    result = is_palindrome_deque(s)
    status = "✓" if result == expected else "✗"
    print(f'{status} is_palindrome_deque("{s}") = {result}')


