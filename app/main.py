from __future__ import annotations
from typing import Any


class Node:
    def __init__(self, key: Any, hash_key: int, value: Any) -> None:
        self.key = key
        self.hash_key = hash_key
        self.value = value


class Dictionary:
    def __init__(self) -> None:
        self._capacity = 8
        self._threshold = 2 / 3
        self._hash_table = [None] * self._capacity
        self._length = 0

    def __setitem__(self, key: Any, value: Any) -> None:
        # оновлення коду
        if self._length / self._capacity > self._threshold:
            self.update()

        # обчислення індексу в хеш-таблиці
        hash_key = hash(key)
        index = hash_key % self._capacity

        # вирішення колізії і однакового ключа
        while self._hash_table[index] is not None:
            node = self._hash_table[index]
            if node.key == key:
                node.value = value
                return
            index += 1
            index %= self._capacity

        # встановлення нового значення
        self._hash_table[index] = Node(key, hash_key, value)
        self._length += 1

    def __getitem__(self, key: Any) -> Any:
        # обчислення індексу в хеш-таблиці
        hash_key = hash(key)
        index = hash_key % self._capacity

        # доступ елемента за індексом
        while self._hash_table[index] is not None:
            node = self._hash_table[index]
            if node.key == key:
                return node.value
            index += 1
            index %= self._capacity

        raise KeyError(f"Key {key} is not found")

    def __len__(self) -> int:
        return self._length

    def clear(self) -> None:
        self._hash_table = [None] * self._capacity

    def __delitem__(self, key: Any) -> None:
        hash_key = hash(key)
        index = hash_key % self._capacity

        while self._hash_table[index] is not None:
            if self._hash_table[index].key == key:
                self._hash_table[index] = None
                self._length -= 1
                return
            index += 1
            index %= self._capacity

        raise KeyError(f"No such key {key}")

    def get(self, key: Any, default: Any = None) -> Any:
        hash_key = hash(key)
        index = hash_key % self._capacity

        while self._hash_table[index] is not None:
            node = self._hash_table[index]
            if node.key == key:
                return node.value
            index += 1
            index %= self._capacity
        return default

    def pop(self, key: Any) -> Any:
        hash_key = hash(key)
        index = hash_key % self._capacity

        while self._hash_table[index] is not None:
            node = self._hash_table[index]
            if node.key == key:
                self._hash_table[index] = None
                self._length -= 1
                return node.value
            index += 1
            index %= self._capacity

    def update(self) -> None:
        # оновленння ємкості та створення оновленої таблиці
        self._capacity *= 2
        new_hash_table = [None] * self._capacity

        for node in self._hash_table:
            # якщо Node не None обчислюємо для неї індекс
            if node is not None:
                index = hash(node.key) % self._capacity
                # вирішенняя колізії
                while new_hash_table[index] is not None:
                    index += 1
                    index %= self._capacity
                # встановлення ноди за індексом
                new_hash_table[index] = node

        self._hash_table = new_hash_table

    def __iter__(self) -> Any:
        for node in self._hash_table:
            if node is not None:
                yield node.key
