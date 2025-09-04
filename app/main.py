from typing import Any


class Dictionary:
    def __init__(self) -> None:
        # Стандартна місткість словника
        self.capacity = 8

        # Кількість елементів які було записано у словник
        self.record = 0

        # Поріг запису після якого словник збільшується
        self.threshold = int(8 * (2 / 3))

        # Створення словника з стандартною кількість місць
        self.dict = [None] * self.capacity

    def __str__(self) -> str:
        # Створюєм придатний для читання словник
        return str([item[:2] for item in self.dict if isinstance(item, tuple)])

    def find_index(self, key: Any) -> int:
        # Створюєм хеш для ключа
        _hash = hash(key)

        # Визначаєм можливий індекс для ключа
        index = _hash % self.capacity - 1

        # Продовжуєм шукати істинний індекс
        for _ in range(self.capacity):

            # Підраховуєм індекс
            index += 1

            # Перезапис індексу якщо той виходить за допустиме значення
            if index > self.capacity - 1:
                index = 0

            # Спроба знайти індекс
            try:
                if self.dict[index][0] == key and self.dict[index][2] == _hash:
                    return index
            # У разі помилки продовжуєм
            except TypeError:
                continue
        # Створення помилки у разі відсутності вказаного ключа
        raise KeyError(f"Key {type(key)} < {key} > not found")

    def __setitem__(self, key: Any, value: Any) -> None:

        # Функція для запису
        def setdict(def_key: Any = key, def_value: Any = value) -> None:

            # Визначаєм хеш для ключа
            _hash = hash(def_key)

            # Індекс елементу списку(із віднятою одиницею)
            index = _hash % self.capacity - 1

            """
            Створюєм значення для елементу списку де:
            1. Ключ
            2. Задане значення
            3. Хеш(ключ)
            """
            dict_value = (def_key, def_value, _hash)

            # Цикл перезапису та запису
            while True:

                # Підрахунок індексу
                index += 1

                # Задаєм 0 індексу, якщо наступний індекс відсутній
                if index > self.capacity - 1:
                    index = 0

                # Спроба перезапису
                try:
                    if (self.dict[index][0] == def_key
                            and self.dict[index][2] == _hash):

                        self.dict[index] = dict_value
                        break

                # Запис нового значення
                except TypeError:
                    if self.dict[index] is None:
                        self.dict[index] = dict_value
                        self.record += 1
                        break

        # Визначаєм чи не потрібно розширювати словник
        if self.record == self.threshold:
            self.capacity *= 2
            self.old_dict = self.dict.copy()
            self.dict = [None] * self.capacity
            self.record = 0

            # Проходимся по кожному записаному елементу для перезапису
            for _dict in self.old_dict:
                if isinstance(_dict, tuple):
                    setdict(*_dict[:2])

            # Запис значення із граничним індексом
            setdict()

            # Видалення словника із старою місткістю
            del self.old_dict
        else:
            # Місткість збільшувати не потрібно, запис значення
            setdict()

    def __getitem__(self, key: Any) -> Any:
        # Повертаєм значення за індексом
        return self.dict[self.find_index(key)][1]

    def __len__(self) -> int:
        # Повертаєм число записаних блоків
        return self.record

    def __delitem__(self, key: Any = None) -> None:
        # Задаєм пусте значення за введеним ключем
        self.dict[self.find_index(key)] = None

    def __iter__(self) -> tuple:
        # Створення об'єкта для ітерації
        return self.__str__()

    def clear(self) -> None:
        # Очищаєм словник шляхом створення пустих блоків
        self.dict = [None] * self.capacity

    def get(self, key: Any) -> Any:
        # Отримуєм значення без помилки
        try:
            return self.__getitem__(key)
        except KeyError:
            return None

    def pop(self, key: Any) -> None:
        # Видаляєм блок за ключем
        self.dict[self.find_index(key)] = None

    def update(self, key_values: list[tuple]) -> None:
        # Перезаписуєм або додаєм вказані елементи
        for key_value in key_values:
            self.__setitem__(*key_value)
