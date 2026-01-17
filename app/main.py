from typing import Any, Hashable, Iterator


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = 0.66
        self.table: list = [None] * self.capacity
        self.length = 0

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.length / self.capacity > self.load_factor:
            self._resize()

        index = hash(key) % self.capacity

        while self.table[index]:
            node_key, _ = self.table[index]
            if node_key == key:
                self.table[index] = (key, value)
                return
            index = (index + 1) % self.capacity

        self.table[index] = (key, value)
        self.length += 1

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity

        while self.table[index]:
            node_key, node_value = self.table[index]
            if node_key == key:
                return node_value
            index = (index + 1) % self.capacity

        raise KeyError(f"Key '{key}' not found.")

    def __len__(self) -> int:
        return self.length

    def _resize(self) -> None:
        self.capacity *= 2
        storage = [*self.table]
        self.table = [None] * self.capacity

        for node in storage:
            if node:
                key, value = node
                new_index = hash(key) % self.capacity
                while self.table[new_index]:
                    new_index = (new_index + 1) % self.capacity
                self.table[new_index] = (key, value)

    def clear(self) -> None:
        self.table = [None] * self.capacity
        self.length = 0

    def __delitem__(self, key: Hashable) -> None:
        index = hash(key) % self.capacity

        while self.table[index]:
            node_key, _ = self.table[index]
            if node_key == key:
                self.table[index] = None
                return
            index = (index + 1) % self.capacity
        raise KeyError(f"Key '{key}' not found.")

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Any, default: Any = None) -> Any:
        try:
            value = self[key]
            self.__delitem__(key)
            return value
        except KeyError:
            return default

    def update(self, other: dict[Hashable, Any]) -> None:
        for key, value in other.items():
            self[key] = value

    def __iter__(self) -> Iterator[Any]:
        for item in self.table:
            if item is not None:
                yield item[0]
