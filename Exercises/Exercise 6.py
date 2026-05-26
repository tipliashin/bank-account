import time


def benchmark(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()

        result = func(*args, **kwargs)

        end = time.perf_counter()
        elapsed = end - start
        print(f"Время выполнения {func.__name__} в секундах {round(elapsed, 4)}")
        return result

    return wrapper


def validate_positive(func):
    def wrapper(*args, **kwargs):

        res = all(arg > 0 for arg in args)
        if not res:
            raise ValueError("Все аргументы должны быть положительными")
        result = func(*args, **kwargs)
        return result

    return wrapper


@benchmark
def slow_function():
    time.sleep(0.1)
    return "Готово"


@validate_positive
def multiply(a, b):
    return a * b


print(slow_function())
print(multiply(141, 5))
print(multiply(-141, 5))
