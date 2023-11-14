from typing import Optional, Hashable


class Node:
    def __init__(
            self,
            key: Hashable,
            hash_value: int,
            value: Hashable
    ) -> None:
        self.key = key
        self.hash_value = hash_value
        self.value = value
        self.next: Optional[Node] = None


class Dictionary:
    def __init__(
            self,
            initial_capacity: int = 16,
            load_factor: float = 0.75
    ) -> None:
        self.capacity: int = initial_capacity
        self.load_factor: float = load_factor
        self.size: int = 0
        self.table: list[Optional[Node]] = [None] * initial_capacity

    def __setitem__(
            self,
            key: Hashable,
            value: Hashable
    ) -> None:
        hash_value: int = hash(key)
        index: int = hash_value % self.capacity

        if self.table[index] is None:
            self.table[index] = Node(key, hash_value, value)
            self.size += 1
        else:
            current: Optional[Node] = self.table[index]
            while current:
                if current.key == key:
                    current.value = value
                    return
                if current.next is None:
                    break
                current = current.next

            current.next = Node(key, hash_value, value)
            self.size += 1

        if self.size > self.capacity * self.load_factor:
            self._resize()

    def __getitem__(self, key: Hashable) -> Hashable:
        index: int = hash(key) % self.capacity
        current: Optional[Node] = self.table[index]

        while current:
            if current.key == key:
                return current.value
            current = current.next

        raise KeyError(f"Key '{key}' not found in the dictionary")

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        new_capacity: int = self.capacity * 2
        new_table: list[Optional[Node]] = [None] * new_capacity

        for node in self.table:
            while node:
                index: int = node.hash_value % new_capacity
                if new_table[index] is None:
                    new_table[index] = Node(
                        node.key,
                        node.hash_value,
                        node.value
                    )
                else:
                    current: Optional[Node] = new_table[index]
                    while current.next:
                        current = current.next
                    current.next = Node(node.key, node.hash_value, node.value)

                node = node.next

        self.table = new_table
        self.capacity = new_capacity
