"""
Вычисление выражения в постфиксной записи
"""


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


class Validator:
    """Класс первичной проверки на корректность введённых данных"""

    @staticmethod
    def is_operand(val: str) -> bool:
        """Проверка, что в строке число и оно больше 0"""
        try:
            return float(val) >= 0
        except ValueError:
            return False

    @staticmethod
    def is_operator(s: str) -> bool:
        """Проеряет, что символ является какой либо оперцией"""
        return s in {"+", "-", "/", "*"}

    @classmethod
    def verification_of_correctness(cls, expression: list) -> bool:
        """Проверка на корректность вводимых данных"""

        # счётчики для подсчёта количества операндов и операций
        operand_count = 0
        operator_count = 0

        for elem in expression:
            if cls.is_operand(elem):
                operand_count += 1
            elif cls.is_operator(elem):
                operator_count += 1
            else:
                return False

        # В постфиксной записи операторов должно быть на 1 меньше, чем операндов
        return operand_count == operator_count + 1


class PostfixCalculator:
    """Класс для вычисления постфиксных выражений."""

    def __init__(self):
        self.stack = Stack()

    def evaluate(self, expression: list):
        """Подсчёт выражения"""

        count = 0  # счётчик знаков операций
        for element in expression:
            # если число, то добавляем в стек
            if Validator.is_operand(element):
                self.stack.push(float(element))
            # если знак операции, вычисляем значение
            elif Validator.is_operator(element):
                count += 1
                second = self.stack.pop()
                first = self.stack.pop()
                if first is None or second is None:
                    print(
                        f"Ошибка: недостаточно операндов для {count} операции: {element}."
                    )
                    return

                if element == "+":
                    self.stack.push(first + second)
                elif element == "-":
                    self.stack.push(first - second)
                elif element == "*":
                    self.stack.push(first * second)
                else:
                    if second == 0:
                        print("На ноль делить нельзя!")
                        return
                    self.stack.push(first / second)

        rezult = self.stack.pop()
        #  проверка что в стеке ещё остались элементы
        if not self.stack.is_empty():
            print("Ошибка: лишние операнды. Выражение не корректно.")
            return
        return rezult


if __name__ == "__main__":
    while True:
        user_input = input(
            "\nВведите выражение в одну строчку через пробел, "
            "содержащее только положительные числа и знаки операций: +, –, *, /, \n"
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

        if Validator.verification_of_correctness(expression):
            rez = PostfixCalculator()
            r = rez.evaluate(expression)
            if not r:
                print("Выражение не корректно.!")
            else:
                print(f"Результат вычислений: {r}")
        else:
            print(
                "Введите корректные данные: только положительные числа "
                "и знаки операций: +, –, *, /."
            )
