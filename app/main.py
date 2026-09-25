from typing import Any, Iterator


class Node:
    def __init__(self, key: Any, value: Any, hash_value: int) -> None:
        self.key = key
        self.value = value
        self.hash = hash_value


class Dictionary:
    INITIAL_CAPACITY = 8
    LOAD_FACTOR = 2 / 3

    def __init__(self) -> None:
        self.capacity = self.INITIAL_CAPACITY
        self.size = 0
        self.hash_table = [None] * self.capacity

    def calculate_index(self, key: Any, capacity: int) -> int:
        return hash(key) % capacity

    def _resize(self) -> None:
        old_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.size = 0

        for node in old_table:
            if node is not None:
                self._insert(node.key, node.value, node.hash)

    def _insert(self, key: Any, value: Any, hash_value: int) -> None:
        index = hash_value % self.capacity

        while self.hash_table[index] is not None:
            node = self.hash_table[index]
            if node.hash == hash_value and node.key == key:
                node.value = value
                return
            index = (index + 1) % self.capacity
        self.hash_table[index] = Node(key, value, hash_value)
        self.size += 1

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.size >= self.capacity * self.LOAD_FACTOR:
            self._resize()

        hash_value = hash(key)
        self._insert(key, value, hash_value)

    def __getitem__(self, key: Any) -> Any:
        hash_value = hash(key)
        index = hash_value % self.capacity

        while self.hash_table[index] is not None:
            node = self.hash_table[index]
            if node.hash == hash_value and node.key == key:
                return node.value
            index = (index + 1) % self.capacity
        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def __delitem__(self, key: Any) -> None:
        hash_value = hash(key)
        index = hash_value % self.capacity

        while self.hash_table[index] is not None:
            node = self.hash_table[index]
            if node.hash == hash_value and node.key == key:
                self.hash_table[index] = None
                self.size -= 1
                self._rehash_cluster(index)
                return
            index = (index + 1) % self.capacity

        raise KeyError(key)

    def _rehash_cluster(self, deleted_index: int) -> None:
        index = (deleted_index + 1) % self.capacity

        while self.hash_table[index] is not None:
            node = self.hash_table[index]
            self.hash_table[index] = None
            self.size -= 1
            self._insert(node.key, node.value, node.hash)
            index = (index + 1) % self.capacity

    def __contains__(self, key: Any) -> bool:
        try:
            self[key]
            return True
        except KeyError:
            return False

    def __iter__(self) -> Iterator[Any]:
        for node in self.hash_table:
            if node is not None:
                yield node.key

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Any, *args: Any) -> Any:
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            if args:
                return args[0]
            raise

    def update(self, other: "Dictionary") -> None:
        for key in other:
            self[key] = other[key]

    def clear(self) -> None:
        self.capacity = self.INITIAL_CAPACITY
        self.si
        self.hash_table = [None] * self.capacity
