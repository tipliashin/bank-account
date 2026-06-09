from collections import deque


class MyQueue():
    def __init__(self):
        self.input_stack = []  # стек для добавления
        self.output_stack = []  # стек для извлечения

    def push(self, x: int) -> None:
        self.input_stack.append(x)

    def pop(self):
        # Если выходной стек пуст, перекладываем всё из входного
        if not self.output_stack:
            while self.input_stack:
                self.output_stack.append(self.input_stack.pop())
        # Теперь на вершине output_stack — самый первый добавленный элемент
        return self.output_stack.pop()

    def peek(self) -> int:
        if not self.output_stack:
            while self.input_stack:
                self.output_stack.append(self.input_stack.pop())
        # Не удаляем элемент, просто смотрим
        return self.output_stack[-1]


    def empty(self) -> bool:
        return not self.input_stack and not self.output_stack


q = MyQueue()
q.push(1)
q.push(2)
q.push(3)
print(q.peek())   # 1
print(q.pop())    # 1
print(q.pop())    # 2
print(q.empty())  # False
print(q.pop())    # 3
print(q.empty())  # True
