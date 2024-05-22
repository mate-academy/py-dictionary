from __future__ import annotations

from typing import Hashable, Any

from app.point import Point


class Dictionary:
    def __init__(self) -> None:
        self.size = 0
        self.capacity = 8
        self.hash_table: list = [None] * self.capacity
        self.load_factor = 2 / 3

    def __setitem__(self, key: Hashable | Point, value: Any) -> None:
        index = hash(key) % self.capacity
        self.update(key, value, index)
        self.size += 1

        if self.size / self.capacity >= self.load_factor:
            self.resize_and_rehash()

    def __getitem__(self, input_key: Hashable | Point) -> Any:
        index = hash(input_key) % self.capacity
        while self.hash_table[index] is not None:
            key, value = self.hash_table[index]
            if key == input_key:
                return value
            index = (index + 1) % self.capacity
        raise KeyError(f"Key '{input_key}' not found.")

    def __len__(self) -> int:
        return self.size

    def update(self, key: Hashable | Point, value: Any, index: int) -> None:
        while self.hash_table[index] is not None:
            if key == self.hash_table[index][0]:
                self.hash_table[index] = (key, value)
                self.size -= 1
                break
            print(f"The key {key} collided with {self.hash_table[index]}")
            index = (index + 1) % self.capacity
        self.hash_table[index] = (key, value)

    def resize_and_rehash(self) -> None:
        tab_to_update = [node for node in self.hash_table if node is not None]
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        for key, value in tab_to_update:
            index = hash(key) % self.capacity
            self.update(key, value, index)
