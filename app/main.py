from typing import Any, Optional, List


class Node:
    def __init__(
            self,
            key: Any,
            value: Any
    ) -> None:
        self.key = key
        self.hash = hash(key)
        self.value = value
        self.next: Optional[Node] = None


class Dictionary:
    def __init__(
            self,
            initial_capacity: int = 8,
            load_factor: float = 2 / 3
    ) -> None:
        self.capacity: int = initial_capacity
        self.load_factor: float = load_factor
        self.size: int = 0
        self.table: List[Optional[Node]] = [None] * self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        index: int = self._hash_index(key)
        if self.table[index] is None:
            self.table[index] = Node(key, value)
        else:
            current: Optional[Node] = self.table[index]
            while current.next:
                if current.key == key:
                    current.value = value
                    return
                current = current.next
            if current.key == key:
                current.value = value
                return
            current.next = Node(key, value)
        self.size += 1
        self._resize_if_needed()

    def __getitem__(
            self,
            key: Any
    ) -> Any:
        index: int = self._hash_index(key)
        current: Optional[Node] = self.table[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next
        raise KeyError(f"Key not found: {key}")

    def __len__(self) -> int:
        return self.size

    def _hash_index(self, key: Any) -> int:
        return hash(key) % self.capacity

    def _resize_if_needed(self) -> None:
        if self.size / self.capacity > self.load_factor:
            self._resize()

    def _resize(self) -> None:
        new_capacity: int = self.capacity * 2
        new_table: List[Optional[Node]] = [None] * new_capacity

        for i in range(self.capacity):
            current: Optional[Node] = self.table[i]
            while current:
                new_index: int = current.hash % new_capacity
                if new_table[new_index] is None:
                    new_table[new_index] = Node(current.key, current.value)
                else:
                    new_current: Optional[Node] = new_table[new_index]
                    while new_current.next:
                        new_current = new_current.next
                    new_current.next = Node(current.key, current.value)

                current = current.next

        self.table = new_table
        self.capacity = new_capacity
