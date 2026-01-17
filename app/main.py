from typing import Any, Optional, List


class Node:
    """Node to store a key–value pair inside hash table."""

    def __init__(self, key: Any, value: Any) -> None:
        self.key: Any = key
        self.hash: int = hash(key)
        self.value: Any = value
        self.next: Optional["Node"] = None


class Dictionary:

    def __init__(
            self,
            initial_capacity: int = 8,
            load_factor: float = 0.75
    ) -> None:
        self.capacity: int = initial_capacity
        self.load_factor: float = load_factor
        self.length: int = 0
        self.table: List[Optional[Node]] = [None] * self.capacity

    def __len__(self) -> int:
        return self.length

    def _get_index(self, key_hash: int) -> int:
        return key_hash % self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        # Resize if needed
        if self.length + 1 > self.capacity * self.load_factor:
            self._resize()

        key_hash = hash(key)
        index = self._get_index(key_hash)
        node = self.table[index]

        # No collision → save directly
        if node is None:
            self.table[index] = Node(key, value)
            self.length += 1
            return

        # Collision → walk linked list
        prev: Optional[Node] = None
        while node:
            if node.key == key:
                node.value = value
                return
            prev = node
            node = node.next

        # Add new node at end
        prev.next = Node(key, value)
        self.length += 1

    def __getitem__(self, key: Any) -> Any:
        key_hash = hash(key)
        index = self._get_index(key_hash)
        node = self.table[index]

        while node:
            if node.key == key:
                return node.value
            node = node.next

        raise KeyError(f"Key not found: {key}")

    def _resize(self) -> None:
        """Double table size and rehash all items."""
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.length = 0  # will re-add all nodes

        for node in old_table:
            while node:
                self[node.key] = node.value
                node = node.next
