from typing import Any, Hashable


class Node:
    def __init__(self, key: Hashable, value: Any) -> None:
        self.key = key
        self.hash = hash(key)
        self.value = value


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.size = 0
        self.backers = [None for _ in range(self.capacity)]

    def _insert_no_resize(self, node: Node) -> None:
        index = node.hash % self.capacity

        for _ in range(self.capacity):
            existing = self.backers[index]
            if existing is None or existing.key == node.key:
                self.backers[index] = node
                break
            index = (index + 1) % self.capacity

    def resize(self) -> None:
        if self.size / self.capacity > 0.75:
            old_backers = self.backers.copy()
            self.capacity *= 2
            self.backers = [None for _ in range(self.capacity)]

            for item in old_backers:
                if isinstance(item, Node):
                    self._insert_no_resize(item)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        self.resize()

        new_item = Node(key, value)
        index = new_item.hash % self.capacity

        for _ in range(self.capacity):
            existing = self.backers[index]

            if existing is None:
                self.backers[index] = new_item
                self.size += 1
                break
            elif existing.key == new_item.key:
                self.backers[index] = new_item
                break
            index = (index + 1) % self.capacity

    def __getitem__(self, item: Hashable) -> Any:
        hash_item = hash(item)
        index = hash_item % self.capacity

        for _ in range(self.capacity):
            node = self.backers[index]
            if node is None:
                break
            if isinstance(node, Node) and item == node.key:
                return node.value
            index = (index + 1) % self.capacity
        raise KeyError(f"Key {item} not found")

    def __len__(self) -> int:
        return self.size
