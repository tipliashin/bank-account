"""
squares = [x**2 for x in range(10)]
print(squares)
sq_dict = {x: x**2 for x in range(5)}
print(sq_dict)
words = ["apple", "banan", "apple", "kiwi"]
lengths = {w for w in words}  # {4, 5, 6}
print(lengths)
"""

list_of_words = input("Введите строку: ")
freq = {}
for char in list_of_words:
    freq[char] = freq.get(char, 0) + 1
sorted_items = sorted(freq.items())
print("Частотный словарь:", dict(sorted_items))
top3 = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:3]
print("Топ-3:", top3)
