from typing import Optional


class Node:
    def __init__(
            self,
            key: any,
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

    def _hash_function(self, key: any) -> int:
        return hash(key)

    def _get_index(self, key: any) -> int:
        hash_value: int = self._hash_function(key)
        return hash_value % self.capacity

    def __setitem__(self, key: any, value: str) -> None:
        index: int = self._get_index(key)
        node: Optional[Node] = self.hash_table[index]

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

    def __getitem__(self, key: any) -> str:
        index: int = self._get_index(key)
        node: Optional[Node] = self.hash_table[index]

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
                # Use the _get_index method for calculating the new index
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
        self.hash_table = new_hash_table
