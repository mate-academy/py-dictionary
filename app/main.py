from typing import Any, Hashable


class Node:
    def __init__(self, key: Hashable, value: Any) -> None:
        self.key = key
        self.value = value
        self.hash = hash(self.key)


class Dictionary:
    def __init__(
            self, initial_capacity: int = 8, load_factor: float = 2 / 3
    ) -> None:
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]

    def __setitem__(self, key: Hashable, value: Any) -> None:
        node = Node(key, value)
        if not self._check_size():
            self._rebuild()
        index = self._calculate_index(node)
        if self.buckets[index]:
            for old in self.buckets[index]:
                if old.key == node.key:
                    old.value = node.value
                    return
        self.buckets[index].append(node)
        self.size += 1

    def __getitem__(self, key: Hashable) -> Any:
        index = self._calculate_index(key)
        if not self.buckets[index]:
            raise KeyError
        for element in self.buckets[index]:
            if element.hash == hash(key):
                if key == element.key:
                    return element.value

    def __len__(self) -> int:
        return self.size

    def _calculate_index(self, node: Node | Hashable) -> int:
        if isinstance(node, Node):
            return node.hash % self.capacity
        return hash(node) % self.capacity

    def _check_size(self) -> bool:
        return self.size < self.capacity * self.load_factor

    def _rebuild(self) -> None:
        self.capacity *= 2
        temp_buckets = self.buckets
        self.buckets = [[] for _ in range(self.capacity)]
        for internal_list in temp_buckets:
            if internal_list:
                for element in internal_list:
                    index = self._calculate_index(element)
                    self.buckets[index].append(element)

    def __delitem__(self, key: Hashable) -> Any:
        index = self._calculate_index(key)
        if not self.buckets[index]:
            raise KeyError
        for node in self.buckets[index]:
            if key == node.key:
                self.buckets[index].remove(node)
                self.size -= 1
                return

    def clear(self) -> None:
        self.buckets.clear()
        self.size = 0

    def __iter__(self) -> Hashable:
        for internal_list in self.buckets:
            for node in internal_list:
                yield node.key
