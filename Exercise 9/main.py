import math_utils

print(math_utils.add(2, 3))  # 5
print(math_utils.PI)


# my_module.py
def helper():
    return "Помощь"


if __name__ == "__main__":
    print("Этот код запущен напрямую")
    print(helper())
