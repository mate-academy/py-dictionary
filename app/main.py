from typing import Any


class Node:
    def __init__(
            self,
            key: Any,
            value: Any
    ) -> None:
        self.key = key
        self.value = value
        self.hash = hash(key)
        self.next: Node = None


class Dictionary:
    def __init__(
            self,
            initial_capacity: int = 8
    ) -> None:
        self.capacity = initial_capacity
        self.size = 0
        self.buckets = [None] * self.capacity

    def _get_bucket_index(self, key: Any) -> int:
        return hash(key) % self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        index = self._get_bucket_index(key)

        if self.buckets[index] is None:
            self.buckets[index] = Node(key, value)
        else:
            current = self.buckets[index]
            while True:
                if current.key == key:
                    current.value = value  # Update value when key exists
                    return
                if current.next is None:
                    break
                current = current.next
            current.next = Node(key, value)

        self.size += 1
        if self.size / self.capacity > 0.7:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        index = self._get_bucket_index(key)
        current = self.buckets[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next
        raise KeyError(f"Key {key} not found")

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_buckets = [None] * new_capacity

        for bucket in self.buckets:
            current = bucket
            while current:
                new_index = hash(current.key) % new_capacity
                if new_buckets[new_index] is None:
                    new_buckets[new_index] = Node(current.key, current.value)
                else:
                    new_node = new_buckets[new_index]
                    while new_node.next:
                        new_node = new_node.next
                    new_node.next = Node(current.key, current.value)
                current = current.next

        self.capacity = new_capacity
        self.buckets = new_buckets

    def __contains__(self, key: Any) -> bool:
        try:
            self[key]
            return True
        except KeyError:
            return False
