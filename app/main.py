from typing import Hashable, Generic, Sequence, TypeVar

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


class Node:
    def __init__(self, key: K, value: V, next_node: "Node" = None) -> None:
        self.key = key
        self.value = value
        self.next = next_node

    def __repr__(self) -> str:
        return f"Node({self.key}, {self.value})"


class Dictionary(Generic[K, V]):
    def __init__(
            self,
            initial_capacity: int = 16,
            load_factor: float = 0.75
    ) -> None:
        self.initial_capacity = initial_capacity
        self.load_factor = load_factor
        self.table: Sequence[Node] = [None] * initial_capacity
        self.size: int = 0

    def __setitem__(self, key: K, value: V) -> None:
        hash_code = hash(key)
        index = hash_code % len(self.table)

        node = self.table[index]
        while node is not None:
            if node.key == key:
                node.value = value
                return
            node = node.next

        new_node = Node(key, value)
        new_node.next = self.table[index]
        self.table[index] = new_node
        self.size += 1

        if self.size / len(self.table) > self.load_factor:
            self._resize()

    def __getitem__(self, key: K) -> V:
        hash_code = hash(key)
        index = hash_code % len(self.table)

        node = self.table[index]
        while node is not None:
            if node.key == key:
                return node.value
            node = node.next

        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        new_table = [None] * (len(self.table) * 2)

        for node in self.table:
            while node is not None:
                next_node = node.next
                hash_code = hash(node.key)
                index = hash_code % len(new_table)

                node.next = new_table[index]
                new_table[index] = node

                node = next_node

        self.table = new_table
