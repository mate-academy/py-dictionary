from __future__ import annotations
from typing import Any


class Dictionary:
    def __init__(self, initial_capacity: int = 8) -> None:
        self.capacity = initial_capacity  # Початкова ємність
        self.size = 0  # Кількість елементів
        self.table = [None] * self.capacity  # Хеш-таблиця

    def __setitem__(self, key: Any, value: Any) -> Any:
        # Визначаємо індекс у таблиці за допомогою хеш-функції
        index = hash(key) % self.capacity

        # Якщо місце вже зайняте, перевіряємо, чи це той самий ключ
        if self.table[index] is not None:
            for i, (k, v) in enumerate(self.table[index]):
                if k == key:
                    self.table[index][i] = (key, value)
                    return
        # Якщо місце порожнє, створюємо новий список кортежів
        if self.table[index] is None:
            self.table[index] = []
        self.table[index].append((key, value))  # Додаємо пару
        self.size += 1

        # Якщо розмір більше, ніж 75% від ємності, збільшуємо таблицю
        if self.size > self.capacity * 0.75:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        # Визначаємо індекс для пошуку
        index = hash(key) % self.capacity
        print(f"Пошук ключа {key} на індексі {index}")  # Додано для дебагу

        # Перевіряємо, чи є елементи на цьому індексі
        if self.table[index] is not None:
            for k, v in self.table[index]:
                if k == key:
                    return v
        raise KeyError(f"Ключ '{key}' не знайдений.")  # Якщо ключ не знайдений

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        # Подвоюємо ємність хеш-таблиці
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0

        for bucket in old_table:
            if bucket is not None:
                for key, value in bucket:
                    self[key] = value

    def __delitem__(self, key: Any) -> None:
        index = hash(key) % self.capacity
        if self.table[index] is not None:
            for i, (k, v) in enumerate(self.table[index]):
                if k == key:
                    del self.table[index][i]
                    self.size -= 1
                    return
        raise KeyError(f"Ключ '{key}' не знайдений для видалення.")

    def get(self, key: Any) -> Dictionary:
        try:
            return self[key]
        except KeyError:
            return None

    def pop(self, key: Any) -> Any:
        index = hash(key) % self.capacity
        if self.table[index] is not None:
            for i, (k, v) in enumerate(self.table[index]):
                if k == key:
                    del self.table[index][i]
                    self.size -= 1
                    return v
        raise KeyError(f"Ключ '{key}' не знайдений для видалення.")

    def __iter__(self) -> None:
        for bucket in self.table:
            if bucket is not None:
                for key, value in bucket:
                    yield key, value

    def __contains__(self, key: Any) -> bool:
        try:
            self[key]
            return True
        except KeyError:
            return False
