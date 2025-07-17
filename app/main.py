from typing import Any


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.hash = hash(key)
        self.value = value


class Dictionary:
    def __init__(self) -> None:
        self._initial_capacity = 8
        self._data = [None] * self._initial_capacity
        self._load_factor = 2 / 3
        self._threshold = int(self._initial_capacity * self._load_factor)

    def update_capacity(self) -> None:
        self._initial_capacity *= 2

    def update_threshold(self) -> None:
        self._threshold = int(self._initial_capacity * self._load_factor)

    def full_update(self) -> None:
        self.update_capacity()
        self.update_threshold()
        new_data = [None] * self._initial_capacity
        for node in self._data:
            if node is not None:
                position = hash(node.key) % self._initial_capacity
                while True:
                    if new_data[position] is None:
                        new_data[position] = node
                        break
                    else:
                        position = (position + 1) % self._initial_capacity
        self._data = new_data

    @property
    def _size(self) -> int:
        return len([element for element in self._data if element is not None])

    def __setitem__(self, key: Any, value: Any) -> None:
        if self._size + 1 >= self._threshold:
            self.full_update()
        position = hash(key) % self._initial_capacity
        while True:
            if self._data[position] is None:
                self._data[position] = Node(key, value)
                break
            elif self._data[position].key == key:
                self._data[position].value = value
                break
            else:
                position = (position + 1) % self._initial_capacity

    def __getitem__(self, key: Any) -> Any:
        for node in self._data:
            if node is not None:
                if node.key == key:
                    return node.value
        raise KeyError

    def __len__(self) -> int:
        return self._size
