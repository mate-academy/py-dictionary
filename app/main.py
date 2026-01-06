from typing import Any, Optional


class Node:
    def __init__(
        self,
        key: Any,
        value: Any,
        hash_value: int,
        next_node: Optional["Node"] = None,
    ) -> None:
        self.key = key
        self.value = value
        self.hash_value = hash_value
        self.next = next_node


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        if capacity <= 0:
            raise ValueError
        self.capacity = capacity
        self.length = 0
        self.slots: list[Optional[Node]] = [None] * capacity

    def _resize(self) -> None:
        old_slots = self.slots
        self.capacity *= 2
        self.slots = [None] * self.capacity
        self.length = 0

        for node in old_slots:
            while node is not None:
                self[node.key] = node.value
                node = node.next

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.length / self.capacity >= 0.7:
            self._resize()

        hash_value = hash(key)
        index = hash_value % self.capacity
        node = self.slots[index]

        if node is None:
            self.slots[index] = Node(key, value, hash_value)
            self.length += 1
            return

        current = node
        while True:
            if current.key == key:
                current.value = value
                return

            if current.next is None:
                current.next = Node(key, value, hash_value)
                self.length += 1
                return

            current = current.next

    def __getitem__(self, key: Any) -> Any:
        hash_value = hash(key)
        index = hash_value % self.capacity
        node = self.slots[index]

        while node is not None:
            if node.key == key:
                return node.value
            node = node.next

        raise KeyError(key)

    def __len__(self) -> int:
        return self.length


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __hash__(self) -> int:
        coordinates = (self.x, self.y)
        return hash(coordinates)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y
