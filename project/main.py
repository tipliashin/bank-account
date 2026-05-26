from utils.file_utils import read_non_empty_lines
from utils.text_utils import count_words

if __name__ == "__main__":
    with open("sample.txt", "w", encoding="utf-8") as f:
        f.write("Hello, world!\n  \nmy name   is Andrey    \n\n")

    for i in read_non_empty_lines("sample.txt"):
        words_counter = count_words(i)
        print(f"Строка '{i}' содержит {words_counter} слов")
