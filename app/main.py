from typing import Any, List, Optional, Iterator


class Dictionary:
    class Node:
        def __init__(self, key: Any, hash_value: int, value: Any) -> None:
            self.key = key
            self.hash_value = hash_value
            self.value = value

    def __init__(self,
                 initial_capacity: int = 8,
                 load_factor: float = 0.75
                 ) -> None:
        self._capacity: int = initial_capacity
        self._load_factor: float = load_factor
        self._size: int = 0
        self._table: List[Optional[Dictionary.Node]] = [None] * self._capacity

    def _hash(self, key: Any) -> int:
        return hash(key)

    def _resize(self) -> None:
        old_table = self._table
        self._capacity *= 2
        self._table = [None] * self._capacity
        self._size = 0

        for node in old_table:
            if node is not None:
                self[node.key] = node.value

    def __setitem__(self, key: Any, value: Any) -> None:
        if self._size / self._capacity >= self._load_factor:
            self._resize()

        hash_value = self._hash(key)
        index = hash_value % self._capacity

        if self._table[index] is None:
            self._table[index] = self.Node(key, hash_value, value)
            self._size += 1
        else:
            node = self._table[index]
            if node.key == key:
                node.value = value
            else:
                original_index = index
                while (self._table[index] is not None
                       and self._table[index].key != key):
                    index = (index + 1) % self._capacity
                    if index == original_index:
                        raise Exception("HashTable is full")

                if self._table[index] is None:
                    self._table[index] = self.Node(key, hash_value, value)
                    self._size += 1
                else:
                    self._table[index].value = value

    def __getitem__(self, key: Any) -> Any:
        hash_value = self._hash(key)
        index = hash_value % self._capacity
        original_index = index

        while self._table[index] is not None:
            if self._table[index].key == key:
                return self._table[index].value
            index = (index + 1) % self._capacity
            if index == original_index:
                break

        raise KeyError(key)

    def __len__(self) -> int:
        return self._size

    def clear(self) -> None:
        self._table = [None] * self._capacity
        self._size = 0

    def __delitem__(self, key: Any) -> None:
        hash_value = self._hash(key)
        index = hash_value % self._capacity

        original_index = index
        while self._table[index] is not None:
            if index == original_index:
                break
            if self._table[index].key == key:
                self._table[index] = None
                self._size -= 1
                next_index = (index + 1) % self._capacity
                while self._table[next_index] is not None:
                    node_to_rehash = self._table[next_index]
                    self._table[next_index] = None
                    self._size -= 1
                    self[node_to_rehash.key] = node_to_rehash.value
                    next_index = (next_index + 1) % self._capacity
                return
            index = (index + 1) % self._capacity
        raise KeyError(key)

    def get(self, key: Any, default: Optional[Any] = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Any, default: Optional[Any] = None) -> Any:
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            if default is not None:
                return default
            raise

    def update(self, other: dict) -> None:
        for key, value in other.items():
            self[key] = value

    def __iter__(self) -> Iterator[Any]:
        for node in self._table:
            if node is not None:
                yield node.key
