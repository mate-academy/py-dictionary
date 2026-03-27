from typing import Hashable, Any


class Node:
    def __init__(self, key: Hashable, hash_value: int, value: Any) -> None:
        self.key = key
        self.hash_value = hash_value
        self.value = value
        self.next = None


class Dictionary:
    def __init__(self,
                 initial_capacity: int = 8,
                 load_factor: int = 2 / 3) -> None:
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.table = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hash_value = hash(key)
        index = hash_value % self.capacity

        if self.table[index] is None:
            self.table[index] = Node(key, hash_value, value)
            self.size += 1
        else:
            current = self.table[index]
            while current:
                if current.key == key:
                    current.value = value
                    return
                if current.next is None:
                    break
                current = current.next
            current.next = Node(key, hash_value, value)
            self.size += 1

        if self.size / self.capacity > self.load_factor:
            self._resize()

    def __getitem__(self, key: Hashable) -> None:
        hash_value = hash(key)
        index = hash_value % self.capacity

        current = self.table[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next

        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_table = [None] * new_capacity

        for i in range(self.capacity):
            current = self.table[i]
            while current:
                index = current.hash_value % new_capacity
                if new_table[index] is None:
                    new_table[index] = Node(
                        current.key,
                        current.hash_value,
                        current.value
                    )
                else:
                    new_node = Node(
                        current.key,
                        current.hash_value,
                        current.value
                    )
                    new_node.next = new_table[index]
                    new_table[index] = new_node

                current = current.next

        self.capacity = new_capacity
        self.table = new_table
