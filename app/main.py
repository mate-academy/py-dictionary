from typing import Any, Iterator


class Node:
    def __init__(self, key: Any, hash_val: int, value: Any) -> None:
        self.key = key
        self.hash = hash_val
        self.value = value


class Dictionary:
    def __init__(
        self, initial_capacity: int = 8, load_factor: float = 0.66
    ) -> None:
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.table: list[list[Node]] = [[] for _ in range(self.capacity)]

    def _get_index(self, hash_val: int) -> int:
        return hash_val % self.capacity

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [[] for _ in range(self.capacity)]
        self.size = 0

        for bucket in old_table:
            for node in bucket:
                self.__setitem__(node.key, node.value)

    def __setitem__(self, key: Any, value: Any) -> None:
        hash_val = hash(key)
        index = self._get_index(hash_val)

        for node in self.table[index]:
            if node.hash == hash_val and node.key == key:
                node.value = value
                return

        self.table[index].append(Node(key, hash_val, value))
        self.size += 1

        if self.size / self.capacity >= self.load_factor:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        hash_val = hash(key)
        index = self._get_index(hash_val)

        for node in self.table[index]:
            if node.hash == hash_val and node.key == key:
                return node.value

        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def __delitem__(self, key: Any) -> None:
        hash_val = hash(key)
        index = self._get_index(hash_val)

        for i, node in enumerate(self.table[index]):
            if node.hash == hash_val and node.key == key:
                del self.table[index][i]
                self.size -= 1
                return
        raise KeyError(key)

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def clear(self) -> None:
        self.size = 0
        self.table = [[] for _ in range(self.capacity)]

    def __iter__(self) -> Iterator[Any]:
        for bucket in self.table:
            for node in bucket:
                yield node.key
