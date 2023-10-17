from typing import Any, Hashable


class Dictionary:
    # визначаємо основні аргументи таблиці: розмір початкової табли,
    # коеф. загруженості, розмір наповнення
    def __init__(
            self,
            capasity: int = 8,
            load_factor: float = 2 / 3,
            size: int = 0,
    ) -> None:
        self.load_factor = load_factor
        self.capasity = capasity
        self.size = size
        # створюємо дефолтну пусту таблицю
        self.table = [None] * self.capasity

    # в цьому методі вираховуємо індекс елемента,
    # за формулою, щоб не поіторювати цю формулу в інших методах
    def hash_func(self, key: Hashable) -> int:
        return hash(key) % self.capasity

    # пишемо основний функціонал, як вираховується місце елемента в таблиці,
    # як відбувається заповнення таблиці
    # проходить перевірка чи немає колізії(комірка зайнята іншим елементом)
    # чи заміна елемента якщо мають одинакові ключі
    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size >= self.capasity * self.load_factor:
            self.resize()  # зміна розміру після перегрузки таблиці
        index = self.find_index(key)
        if self.table[index] is None:
            self.size += 1
        self.table[index] = [key, value, hash(key)]

    def find_index(self, key: Hashable) -> int:
        index_key = self.hash_func(key)
        while (self.table[index_key] is not None
               and self.table[index_key][0] != key):

            index_key += 1
            index_key %= self.capasity
        return index_key

    # прописуємо розширення таблиці при заповненні на 2/3
    def resize(self) -> None:
        old_table = self.table
        self.capasity *= 2
        self.table = [None] * self.capasity

        self.size = 0
        for item in old_table:
            if item is not None:
                self[item[0]] = item[1]

    # повернення значення при запиті по ключу,
    # якщо такого ключа немає, викидає помилку
    def __getitem__(self, key: Hashable) -> Any:
        index = self.find_index(key)
        if self.table[index] is None:
            raise KeyError(f"Key '{key}' not found in the dictionary")
        return self.table[index][1]

    # довжина таблиці із заповненими елементами
    def __len__(self) -> int:
        return self.size

    # видалення елемента по ключу
    def __delitem__(self, key: Hashable) -> None:
        index_key = self.hash_func(key)
        if self.table[index_key][0] == key:
            del self.table[index_key]
            self.size -= 1

    # очистка таблиці до дефолтних значень
    def clear(self) -> None:
        self.capasity = 8
        self.table = []
        self.size = 0
