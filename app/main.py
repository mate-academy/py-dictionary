from typing import Any, Hashable


class Node:
    def __init__(
            self,
            key: Hashable,
            value: Any,
            hash_value: int
    ) -> None:
        self.key = key
        self.value = value
        self.hash = hash_value
        self.next = None


class Dictionary:
    def __init__(self, capacity: int = 8, load_factor: float = 2 / 3) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.size = 0
        self.table = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hash_value = hash(key)
        index = hash_value % self.capacity

        if self.table[index] is None:
            self.table[index] = Node(key, value, hash_value)
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

            current.next = Node(key, value, hash_value)
            self.size += 1

        if self.size / self.capacity >= self.load_factor:
            self._resize()

    def __getitem__(self, key: Hashable) -> None:
        hash_value = hash(key)
        index = hash_value % self.capacity

        current = self.table[index]
        while current:
            if current.hash == hash_value and current.key == key:
                return current.value
            current = current.next

        raise KeyError(f"Key '{key}' not found")

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_table = [None] * new_capacity

        for i in range(self.capacity):
            current = self.table[i]
            while current:
                new_index = current.hash % new_capacity
                if new_table[new_index] is None:
                    new_table[new_index] = Node(
                        current.key,
                        current.value,
                        current.hash
                    )
                else:
                    new_node = new_table[new_index]
                    while new_node.next:
                        new_node = new_node.next
                    new_node.next = Node(
                        current.key,
                        current.value,
                        current.hash
                    )
                current = current.next

        self.table = new_table
        self.capacity = new_capacity

    def clear(self) -> None:
        self.capacity = 8
        self.size = 0
        self.table = [None] * self.capacity

    def __delitem__(self, key: Hashable) -> None:
        hash_value = hash(key)
        index = hash_value % self.capacity

        current = self.table[index]
        previous = None
        while current:
            if current.key == key:
                if previous:
                    previous.next = current.next
                else:
                    self.table[index] = current.next
                self.size -= 1
                return
            previous = current
            current = current.next

        raise KeyError(f"Key '{key}' not found")

    def get(self, key: Hashable) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return None

    def pop(self, key: Hashable, default: Any = None) -> None:
        try:
            self.__delitem__(key)
            return self.__getitem__(key)
        except KeyError:
            return default

    def update(self, other_dict: dict) -> None:
        for key, value in other_dict.items():
            self[key] = value

    def __iter__(self) -> None:
        for i in self.table:
            current = i
            while current:
                yield current.key
                current = current.next
