from copy import copy
from typing import Union, Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.load_factor = round(self.capacity * 2 / 3)
        self.table = [[] for i in range(self.capacity)]  # [[key, hash, value]]

    def _resize(self) -> None:
        temp = copy(self.table)
        self.capacity *= 2
        self.length = 0
        self.load_factor = round(self.capacity * 2 / 3)
        self.table = [[] for i in range(self.capacity)]

        for node in temp:
            if node:
                self.__setitem__(node[0], node[2])

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.length > self.load_factor:
            self._resize()

        index = hash(key) % self.capacity
        key_index = self.get_index(key)

        if key_index is not None:
            self.table[key_index] = [key, hash(key), value]
            return

        for i in range(self.capacity):
            node = self.table[index]

            if node:
                index = (index + 1) % self.capacity
            else:
                self.table[index] = [key, hash(key), value]
                self.length += 1
                break

    def get_index(self, key: Hashable) -> Union[int, None]:
        index = hash(key) % self.capacity

        for _ in range(self.capacity):
            node = self.table[index]

            if node and node[1] == hash(key) and node[0] == key:
                return index

            index = (index + 1) % self.capacity

        return None

    def __getitem__(self, key: Hashable) -> Any:
        index = self.get_index(key)
        if index is not None:
            return self.table[index][2]

        raise KeyError

    def __len__(self) -> int:
        return self.length

    def clear(self) -> None:
        self.length = 0
        self.capacity = 8
        self.load_factor = round(self.capacity * 2 / 3)
        self.table = [[] for i in range(self.length)]

    def __delitem__(self, key: Hashable) -> list | None:
        index = self.get_index(key)
        if index is not None:
            self.table[index] = []
            self.length -= 1
            return
        raise KeyError

    def pop(self, key: Hashable) -> list | None:
        index = self.get_index(key)
        if index is not None:
            node = self.table[index]
            self.__delitem__(key)
            return node[2]
        return None

    def update(self, key: Hashable, value: Any) -> None:
        index = self.get_index(key)

        if index is not None:
            node = self.table[index]
            node[2] = value
            return

        raise KeyError

    def __repr__(self) -> str:
        result = ["Dictionary:"]

        if not self.length:
            return "Dictionary: ()"

        for i in range(self.capacity):
            node = self.table[i]
            if node:
                key, _, value = node
                result.append(f"(Point({key.x, key.y}): {value})")
        return " ".join(result)
