from dataclasses import dataclass
from typing import Hashable, Any, Optional


@dataclass
class Node:
    key: Hashable
    value: Any
    hash_num: int


class Dictionary:
    INITIAL_CAPACITY = 8
    THRESHOLD = 2 / 3.0
    CAPACITY_MULTIPLIER = 2

    def __init__(self, capacity: int = INITIAL_CAPACITY) -> None:
        self.capacity = capacity
        self.size = 0
        self.hash_table: list[Optional[Node]] = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> object:
        hash_value = hash(key)
        index_value = hash_value % self.capacity

        # Перевірка наявності ключа на обчисленому індексі
        while self.hash_table[index_value] is not None:
            # Якщо знайдено ключ, оновлюємо значення
            if self.hash_table[index_value].key == key:
                self.hash_table[index_value].value = value
                return
            # Якщо ключ не той, рухаємось до наступного індексу
            index_value = (index_value + 1) % self.capacity

        # Додаємо новий вузол, якщо ключ не знайдений
        new_node = Node(key, value, hash_value)
        self.hash_table[index_value] = new_node

        self.size += 1

        # Перевірка на завантаженість
        if self.size / self.capacity > self.THRESHOLD:
            self._resize()

    def _resize(self) -> None:
        new_capacity = self.capacity * self.CAPACITY_MULTIPLIER  # Новий розмір
        new_hash_table: list[Optional[Node]] = [None] * new_capacity
        # Перенесемо старі вузли в нову таблицю
        for node in self.hash_table:
            if node is not None:  # Якщо вузол не None
                # Обчислюємо новий індекс
                hash_value = node.hash_num
                index_value = hash_value % new_capacity

                # Лінійне пробування для знаходження вільного місця
                while new_hash_table[index_value] is not None:
                    index_value = (index_value + 1) % new_capacity

                # Додаємо вузол до нової таблиці
                new_hash_table[index_value] = node

        # Оновлюємо атрибути
        self.capacity = new_capacity
        self.hash_table = new_hash_table

    def __getitem__(self, key: Hashable) -> Any:
        hash_value = hash(key)
        index_value = hash_value % self.capacity

        # Пошук значення за ключем
        while self.hash_table[index_value] is not None:
            if self.hash_table[index_value].key == key:
                return self.hash_table[index_value].value
            index_value = (index_value + 1) % self.capacity

        # Якщо ключ не знайдений, викликаємо виключення
        raise KeyError(f"Key '{key}' not found.")

    def __len__(self) -> int:
        return self.size
