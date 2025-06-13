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
            newnode = NodeList(data)  # создаём новый узел
            newnode.next_el = self.top  # связываем его с текущей вершиной
            self.top = newnode  # переназначаем вершину

    def pop(self):
        """Удалить с вершины"""
        if self.is_empty():
            return None
        else:
            poppednode = self.top  # сохраняем текущую вершину
            self.top = self.top.next_el  # переносим указатель к следующему элементу
            poppednode.next_el = None  # разрываем связь вершины со стеком
            return poppednode.data  # возвращаем значение удаленной вершины


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
    def verification_of_correctness(cls, expression: list[str]) -> bool:
        """Проверка на корректность вводимых данных"""

        # счётчики для подсчёта количества операндов и операций
        operand_count = 0
        operator_count = 0

        for elem in expression:
            if cls.is_operand(elem):  # если число
                operand_count += 1
            elif cls.is_operator(elem):  # если знак операции
                operator_count += 1
            else:  # если не то и не другое - это некорректный элемент
                raise ValueError(f"Некорректный элемент {elem}")

        # В постфиксной записи операторов должно быть на 1 меньше, чем операндов
        if operand_count == operator_count + 1:
            return True
        else:
            raise ValueError(
                "Некорректный ввод. Количество чисел должно быть на 1 больше, чем операций!"
            )


class PostfixCalculator:
    """Класс для вычисления постфиксных выражений."""

    @staticmethod
    def evaluate(expression: list[str]) -> float:
        """Подсчёт выражения"""
        stack = Stack()
        count = 0  # счётчик знаков операций
        for element in expression:
            # если число, то добавляем в стек
            if Validator.is_operand(element):
                stack.push(float(element))
            # если знак операции, вычисляем значение
            elif Validator.is_operator(element):
                count += 1
                second = stack.pop()
                first = stack.pop()
                # если закончились элементы в стеке
                if first is None or second is None:
                    raise ValueError(
                        f"Недостаточно операндов для {count} операции '{element}' !"
                    )

                if element == "+":
                    stack.push(first + second)
                elif element == "-":
                    stack.push(first - second)
                elif element == "*":
                    stack.push(first * second)
                else:
                    if second == 0:
                        raise ValueError("Деление на 0!")
                    stack.push(first / second)
            else:
                raise ValueError(f"Некорректный элемент {element}!")

        result = stack.pop()  # достам элемент после всего прохода
        #  проверка что в стеке ещё остались элементы
        if not stack.is_empty():
            raise ValueError("Лишние операнды в стеке!")
        return result


if __name__ == "__main__":
    # программа выполняется до тех пор пока не будет введено exit
    while True:
        user_input = input(
            "\nВведите выражение в одну строчку через пробел, "
            "содержащее только положительные числа и знаки операций: +, –, *, /, \n"
            "либо 'exit' для выхода: \n"
        )
        # удвляем пробелы и преобразуем к строчным
        if user_input.strip().lower() == "exit":
            break

        # если пустой ввод
        if not user_input:
            print("Пустой ввод. Повторите попытку.")
            continue

        # разделяем элементы по пробелам
        expression = user_input.split()

        # сначала пытаемся проверить на корректность
        try:
            if Validator.verification_of_correctness(expression):
                # пытаемся вычислить значение
                try:
                    result = PostfixCalculator().evaluate(expression)
                    print(f"Результат: {result}")
                # если вышла ошибка при попытке вычислить
                except ValueError as e:
                    print(f"Ошибка: {e}")  # вывод названия ошибки
        # есливышла ошибка при попытке проверить корректность
        except ValueError as e:
            print(f"Ошибка: {e}")
