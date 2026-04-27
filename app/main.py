from typing import Any, Optional, Iterator


_NO_DEFAULT = object()


class Node:
    def __init__(self, key: Any, hash_val: int, value: Any) -> None:
        self.key = key
        self.hash = hash_val
        self.value = value


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.size = 0
        self.table: list[Optional[Node]] = [None] * self.capacity

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table: list[Optional[Node]] = [None] * self.capacity
        self.size = 0

        for node in old_table:
            if node is not None:
                self.__setitem__(node.key, node.value)

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.size / self.capacity >= 0.66:
            self._resize()

        hash_val = hash(key)
        index = hash_val % self.capacity

        while self.table[index] is not None:
            if self.table[index].key == key:
                self.table[index].value = value
                return
            index = (index + 1) % self.capacity

        self.table[index] = Node(key, hash_val, value)
        self.size += 1

    def __getitem__(self, key: Any) -> Any:
        hash_val = hash(key)
        index = hash_val % self.capacity

        while self.table[index] is not None:
            if self.table[index].key == key:
                return self.table[index].value
            index = (index + 1) % self.capacity
        raise KeyError(f"Key {key} not found in dictionary")

    def clear(self) -> None:
        self.capacity = 8
        self.size = 0
        self.table: list[Optional[Node]] = [None] * self.capacity

    def __delitem__(self, key: Any) -> None:
        hash_val = hash(key)
        index = hash_val % self.capacity

        while self.table[index] is not None:
            if self.table[index].key == key:
                self.table[index] = None
                self.size -= 1

                index = (index + 1) % self.capacity
                while self.table[index] is not None:
                    node_to_rehash = self.table[index]
                    self.table[index] = None
                    self.size -= 1
                    self.__setitem__(node_to_rehash.key, node_to_rehash.value)
                    index = (index + 1) % self.capacity
                return
            index = (index + 1) % self.capacity
        raise KeyError(f"Key {key} not found in dictionary")

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def pop(self, key: Any, default: Any = _NO_DEFAULT) -> Any:
        try:
            popped_value = self.__getitem__(key)
            self.__delitem__(key)
            return popped_value
        except KeyError:
            if default is not _NO_DEFAULT:
                return default
            raise KeyError(f"Key {key} not found in dictionary")

    def update(self, other: Any) -> None:
        if hasattr(other, "items"):
            for key, value in other.items():
                self.__setitem__(key, value)
        else:
            for key, value in other:
                self.__setitem__(key, value)

    def __iter__(self) -> Iterator[Any]:
        for node in self.table:
            if node is not None:
                yield node.key
