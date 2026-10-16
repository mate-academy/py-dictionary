from typing import Any


class Dictionary:
    class Node:
        def __init__(self, key: Any, value: Any) -> None:
            self.key = key
            self.value = value
            self.next = None
            self.hash = hash(key)

    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.count = 0
        self.buckets: list["Dictionary.Node | None"] = [None] * capacity

    def _hash_key(self, key: Any) -> int:
        return hash(key) % self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.count >= self.capacity * 0.75:
            self._resize(self.capacity * 2)
        index = self._hash_key(key)
        if self.buckets[index] is None:
            self.count += 1
            self.buckets[index] = self.Node(key, value)
        else:
            current = self.buckets[index]
            while current:
                if current.key == key:
                    current.value = value
                    return
                if current.next is None:
                    break
                current = current.next
            current.next = self.Node(key, value)
            self.count += 1

    def __getitem__(self, key: Any) -> Any:
        index = self._hash_key(key)
        current = self.buckets[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next
        raise KeyError(key)

    def __len__(self) -> int:
        return self.count

    def _resize(self, new_capacity: int) -> None:
        old_buckets = self.buckets
        self.capacity = new_capacity
        self.buckets = [None] * self.capacity
        for bucket in old_buckets:
            current = bucket
            while current:
                next_node = current.next
                current.next = None
                index = current.hash % self.capacity

                if self.buckets[index] is None:
                    self.buckets[index] = current
                else:
                    tail = self.buckets[index]
                    while tail.next:
                        tail = tail.next
                    tail.next = current

                current = next_node
