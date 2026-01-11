from typing import Any, Hashable, List, Optional


class Node:
    def __init__(self, key: Hashable, value: Any, hash_val: int) -> None:
        self.key = key
        self.value = value
        self.hash = hash_val
        self.next: Optional["Node"] = None


class Dictionary:
    def __init__(
        self, initial_capacity: int = 8, load_factor: float = 2 / 3
    ) -> None:
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.buckets: List[Optional[Node]] = [None] * self.capacity

    def __hash_function(self, key: Hashable) -> int:
        return hash(key)

    def __get_index(self, hash_val: int) -> int:
        return hash_val % self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hash_val = self.__hash_function(key)
        index = self.__get_index(hash_val)
        node = self.buckets[index]
        while node:
            if node.hash == hash_val and node.key == key:
                node.value = value
                return
            node = node.next
        new_node = Node(key, value, hash_val)
        new_node.next = self.buckets[index]
        self.buckets[index] = new_node
        self.size += 1
        if self.size / self.capacity >= self.load_factor:
            self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        hash_val = self.__hash_function(key)
        index = self.__get_index(hash_val)
        node = self.buckets[index]
        while node:
            if node.hash == hash_val and node.key == key:
                return node.value
            node = node.next
        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [None] * self.capacity
        self.size = 0
        for node in old_buckets:
            while node:
                self.__setitem__(node.key, node.value)
                node = node.next

    def __str__(self) -> str:
        pairs = []
        for node in self.buckets:
            while node:
                pairs.append(f"{repr(node.key)}: {repr(node.value)}")
                node = node.next
        return "{" + ", ".join(pairs) + "}"
