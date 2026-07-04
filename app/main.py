from typing import Any, Iterator, List, Optional


class Node:
    def __init__(
            self,
            key: Any,
            value: Any,
            hash_code: int
    ) -> None:
        self.key = key
        self.value = value
        self.hash = hash_code
        self.next: Optional["Node"] = None


class Dictionary:
    def __init__(self) -> None:
        self.capacity: int = 8
        self.size: int = 0
        self.table: List[Optional[Node]] = [None] * self.capacity
        self.load_factor_threshold: float = 0.75

    def _hash(self, key: Any) -> int:
        return hash(key) % self.capacity

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0

        for head_node in old_table:
            current = head_node
            while current:
                self.__setitem__(current.key, current.value)
                current = current.next

    def __setitem__(self, key: Any, value: Any) -> None:
        index = self._hash(key)
        current = self.table[index]

        if current is None:
            self.table[index] = Node(key, value, hash(key))
            self.size += 1
        else:
            prev = None
            while current:
                if current.key == key:
                    current.value = value
                    return
                prev = current
                current = current.next

            prev.next = Node(key, value, hash(key))
            self.size += 1

        if self.size / self.capacity >= self.load_factor_threshold:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        index = self._hash(key)
        current = self.table[index]

        while current:
            if current.key == key:
                return current.value
            current = current.next

        raise KeyError(f"KeyError: Key '{key}' not found.")

    def __len__(self) -> int:
        return self.size

    def __delitem__(self, key: Any) -> None:
        index = self._hash(key)
        current = self.table[index]
        prev = None

        while current:
            if current.key == key:
                if prev is None:
                    self.table[index] = current.next
                else:
                    prev.next = current.next
                self.size -= 1
                return
            prev = current
            current = current.next

        raise KeyError(f"KeyError: Key '{key}' not found.")

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def clear(self) -> None:
        self.capacity = 8
        self.size = 0
        self.table = [None] * self.capacity

    def __iter__(self) -> Iterator:
        for head_node in self.table:
            current = head_node
            while current:
                yield current.key
                current = current.next
