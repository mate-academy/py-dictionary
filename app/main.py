from typing import Any
from dataclasses import dataclass


class Dictionary:
    _DEFAULT_LENGTH = 8
    _LENGTH_RESIZE_COEFFICIENT = 2 / 3
    _RESIZE_MULTIPLY_COEFFICIENT = 2

    @dataclass()
    class _Node:
        key: Any
        value: object
        hash_: int

    def __init__(self):
        self._container = [None for _ in range(self._DEFAULT_LENGTH)]
        self._length = 0
        self._current_length = len(self._container)

    def __setitem__(self, key, value):
        capacity = int(self._LENGTH_RESIZE_COEFFICIENT * self._current_length)
        hash_ = hash(key)
        index = hash_ % self._current_length

        while self._container[index % self._current_length] is not None:
            if index == self._current_length:
                index = 0

            if self._container[index].key == key and hash_ == hash(key):
                self._container[index].value = value
                return
            index += 1

        self._container[index % self._current_length] =\
            self._Node(key, value, hash_)
        self._length += 1

        if capacity <= self._length:
            self.resize()

    def __getitem__(self, key):
        position = hash(key)
        index = 0

        while index < self._current_length:
            if self._container[position % self._current_length].key == key:
                return self._container[position % self._current_length].value
            index += 1
            position += 1
        raise KeyError(key)

    def __len__(self):
        return self._length

    def resize(self):
        self._current_length *= self._RESIZE_MULTIPLY_COEFFICIENT
        self._length = 0
        new_list = self._container.copy()

        self._container = [None for _ in range(self._current_length)]
        for item in new_list:
            if item is not None:
                self.__setitem__(item.key, item.value)


if __name__ == "__main__":
    items = [(f"Element {i}", i) for i in range(1000)]
    dictionary = Dictionary()
    for key, value in items:
        dictionary[key] = value
