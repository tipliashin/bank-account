def calculate(op, *args):
    if op == "+":
        result = 0
        for x in args:
            result += x
        return result
    elif op == "*":
        result = 1
        for x in args:
            result *= x
        return result
    elif op == "max":
        return max(args)
    elif op == "min":
        return min(args)
    else:
        return None


def create_logger(prefix):
    def add_pref(message):
        print(f"[{prefix}] {message}")

    return add_pref


def apply_twice(func, value):
    return func(func(value))


def add_one(x):
    return x + 5


print(apply_twice(add_one, 5))

error_log = create_logger("ERROR")
error_log("File not found")

numbers = list(map(int, input("Enter numbers: ").split()))
operation = input("Choose operation(+, *, max, min): ")

print(calculate(operation, *numbers))
