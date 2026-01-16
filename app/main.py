from dataclasses import dataclass
from typing import Any, List, Optional


@dataclass
class Node:
    hash: int
    key: Any
    value: Any


class Dictionary:
    TABLE_LENGTH = 8
    RESIZE_COEFFICIENT = 2 / 3
    MULTIPLYING_COEFFICIENT = 2

    def __init__(self):
        self._table: List[Optional[Node]] = \
            [None for _ in range(Dictionary.TABLE_LENGTH)]
        self._size = 0
        self._capacity = Dictionary.TABLE_LENGTH

    def _resize(self):
        existing_instances = [
            instance for instance in self._table
            if instance is not None
        ]
        self._capacity *= Dictionary.MULTIPLYING_COEFFICIENT
        self._table = [None for _ in range(self._capacity)]
        self._size = 0

        for instance in existing_instances:
            self.__setitem__(instance.key, instance.value)

    def __setitem__(self, key, value):
        hash_ = hash(key)
        if (self._size + 1) > Dictionary.RESIZE_COEFFICIENT * \
                self._capacity:
            self._resize()
        index_in_table = hash_ % self._capacity

        while self._table[index_in_table] is not None:
            current_instance = self._table[index_in_table]
            if hash_ == current_instance.hash and key == \
                    current_instance.key:
                current_instance.value = value
                return
            index_in_table = (index_in_table + 1) % self._capacity

        self._table[index_in_table] = Node(hash_, key, value)
        self._size += 1

    def __getitem__(self, key):
        hash_ = hash(key)
        index_in_table = hash_ % self._capacity

        while self._table[index_in_table] is not None:
            current_instance = self._table[index_in_table]
            if hash_ == current_instance.hash and key == \
                    current_instance.key:
                return current_instance.value
            index_in_table = (index_in_table + 1) % self._capacity

        raise KeyError(key)

    def __delitem__(self, key):
        hash_ = hash(key)
        index_in_table = hash_ % self._capacity
        if self._table[index_in_table] is not None:
            current_instance = self._table[index_in_table]
            if hash_ == current_instance.hash and key == \
                    current_instance.key:
                del self._table[index_in_table]
                self._size -= 1
                return

        raise KeyError(key)

    def __len__(self):
        return self._size

    def __str__(self):
        message = [
            (instance.key, instance.value)
            for instance in self._table if instance is not None
        ]
        return f"{message}"
