class NodeList:
    """Узел Стека."""
    def __init__(self, data=None, next_el=None):
        self.data = data
        self.next_el = next_el


class Stack:
    """Стек"""

    def __init__(self):
        self.top = None

    def is_empty(self):
        """Проверка, пуст ли стек"""
        return self.top is None

    def push(self, data):
        """Добавить элемент на вершину стека"""
        if self.is_empty():
            self.top = NodeList(data)
        else:
            newnode = NodeList(data)
            newnode.next_el = self.top
            self.top = newnode

    def pop(self):
        """Удалить с вершины"""
        if self.is_empty():
            return None
        else:
            poppednode = self.top
            self.top = self.top.next_el
            poppednode.next_el = None
            return poppednode.data


def is_digit(val) -> bool:
    """Проверка, что в строке число и оно больше 0"""
    try:
        return float(val) > 0
    except ValueError:
        return False


def verification_of_correctness(e: list) -> bool:
    """Проверка на корректность вводимых данных"""
    for i in e:
        if not (i in {"+", "-", "/", "*"} or is_digit(i)):
            return False
    return True


def evaluate_postfix(expression):
    """Подсчёт выражения"""

    stack = Stack()
    count = 0  # счётчик знаков операций
    for element in expression:
        if element not in {"+", "-", "/", "*"}:
            element = float(element)  # преобразов к вещественному
        # если число, добавляем в стек
        if isinstance(element, float):
            stack.push(element)
        # если знак операции, вычисляем значение
        else:
            count += 1
            second = stack.pop()
            first = stack.pop()
            if first is None or second is None:
                print(
                    f"Ошибка: недостаточно операндов для {count} операции: {element}."
                )
                return None
            if element == "+":
                stack.push(first + second)
            elif element == "-":
                stack.push(first - second)
            elif element == "*":
                stack.push(first * second)
            else:
                if second == 0:
                    print("На ноль делить нельзя!")
                    return
                stack.push(first / second)

    rezult = stack.pop()
    #  проверка что в стеке ещё остались элементы
    if not stack.is_empty():
        print("Ошибка: лишние операнды. Выражение не корректно.")
        return
    return rezult


def main():
    """Обработка  выражения"""
    while True:
        user_input = input(
            "\nВведите выражение в одну строчку через пробел, содержащее только положительные числа и знаки операций: +, –, *, /, \n"
            "либо 'exit' для выхода: \n"
        )

        if (
            user_input.strip().lower() == "exit"
        ):  # удвляем пробелы и преобразуем к строчным
            break
        
        # если пустой ввод
        if not user_input:
            print("Пустой ввод. Повторите попытку.")
            continue

        expression = user_input.split()

        if verification_of_correctness(expression):
            rez = evaluate_postfix(expression)
            if rez is None:
                print("Выражение не корректно.!")
            else:
                print(f"Результат вычислений: {rez}")
        else:
            print(
                "Введите корректные данные: только положительные числа и знаки операций: +, –, *, /."
            )
         

if __name__ == "__main__":
    main()
