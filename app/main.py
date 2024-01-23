from typing import Optional, Hashable


class Node:
    def __init__(
            self,
            key: Hashable,
            hash_value: int,
            value: str,
            next_node: Optional["Node"] = None
    ) -> None:
        self.key = key
        self.hash_value = hash_value
        self.value = value
        self.next_node = next_node


class Dictionary:
    def __init__(self) -> None:
        self.length: int = 0
        self.capacity: int = 8
        self.load_factor: float = 0.75
        self.hash_table: list[Optional[Node]] = [None] * self.capacity

    def _hash_function(self, key: Hashable) -> int:
        return hash(key)

    def _get_index(self, key: Hashable) -> int:
        hash_value = self._hash_function(key)
        return hash_value % self.capacity

    def __setitem__(self, key: Hashable, value: str) -> None:
        index: int = self._get_index(key)

        if index >= self.capacity:
            load_factor = self.length / self.capacity
            if load_factor > 0.75:
                self._resize()
                index = self._get_index(key)

        node = self.hash_table[index]

        while node:
            if node.key == key:
                node.value = value
                return
            node = node.next_node

        new_node = Node(
            key,
            self._hash_function(key),
            value,
            self.hash_table[index]
        )
        self.hash_table[index] = new_node
        self.length += 1

    def __getitem__(self, key: Hashable) -> str:
        index = self._get_index(key)
        node = self.hash_table[index]

        while node:
            if node.key == key:
                return node.value
            node = node.next_node

        raise KeyError(f"Key not found: {key}")

    def __len__(self) -> int:
        return self.length

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_hash_table = [None] * new_capacity

        for node in self.hash_table:
            while node:
                new_index = self._get_index(node.key)
                new_node = Node(
                    node.key,
                    node.hash_value,
                    node.value,
                    new_hash_table[new_index]
                )
                new_hash_table[new_index] = new_node
                node = node.next_node

        self.capacity = new_capacity
        self.load_factor = 0.75
        self.hash_table = new_hash_table
