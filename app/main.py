from typing import Any, Hashable


class Node:
    def __init__(
            self,
            key: Hashable,
            hash_key: int,
            value: Any
    ) -> None:
        self.key = key
        self.hash_key = hash_key
        self.value = value
        self.next = None


class Dictionary:
    def __init__(self, capacity: int = 8, load_factor: float = 2 / 3) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.size = 0
        self.table = [None] * capacity

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
                elif current.next is None:
                    break
                current = current.next
            current.next = Node(key, hash_value, value)
            self.size += 1

        if self.size > self.capacity * self.load_factor:
            self.resize()

    def __getitem__(self, key: Hashable) -> Any:
        hash_value: int = hash(key)
        index: int = hash_value % self.capacity

        current = self.table[index]
        while current:
            if current.key == key and current.hash_key == hash_value:
                return current.value
            current = current.next
        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def resize(self) -> None:
        new_capacity = self.capacity * 2
        new_table = [None] * new_capacity

        for element in self.table:
            while element.key:
                hash_value = hash(element.key)
                new_index = hash_value % new_capacity
                if new_table[new_index] is None:
                    new_table[new_index] = Node(element.key,
                                                hash_value,
                                                element.value)
                else:
                    current = new_table[new_index]
                    while current:
                        if current.key == element.key:
                            current.value = element.value
                            return
                        elif current.next is None:
                            break
                        current = current.next
                    current.next = Node(element.key, hash_value, element.value)
        self.table = new_table
