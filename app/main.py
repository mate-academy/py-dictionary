from typing import Any


class Node:
    def __init__(
        self,
        key: Any,
        value: Any,
        key_hash: int
    ) -> None:
        self.key = key
        self.value = value
        self.hash = key_hash
        self.next = None


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.length = 0
        self.load_factor = 0.75
        self.hash_table = [None] * self.capacity

    def __len__(self) -> int:
        return self.length

    def _get_index(self, key_hash: int) -> int:
        return key_hash % self.capacity

    def _resize(self) -> None:
        old_table = self.hash_table

        self.capacity *= 2
        self.hash_table = [None] * self.capacity

        old_length = self.length
        self.length = 0

        for node in old_table:
            current = node

            while current is not None:
                self[current.key] = current.value
                current = current.next

        self.length = old_length

    def __setitem__(self, key: Any, value: Any) -> None:
        key_hash = hash(key)
        index = self._get_index(key_hash)

        current = self.hash_table[index]

        while current is not None:
            if current.key == key:
                current.value = value
                return

            current = current.next

        new_node = Node(key, value, key_hash)

        new_node.next = self.hash_table[index]
        self.hash_table[index] = new_node

        self.length += 1

        if self.length / self.capacity >= self.load_factor:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        key_hash = hash(key)
        index = self._get_index(key_hash)

        current = self.hash_table[index]

        while current is not None:
            if current.key == key:
                return current.value

            current = current.next

        raise KeyError(f"Key '{key}' not found")

    def __delitem__(self, key: Any) -> None:
        key_hash = hash(key)
        index = self._get_index(key_hash)

        current = self.hash_table[index]
        previous = None

        while current is not None:
            if current.key == key:
                if previous is None:
                    self.hash_table[index] = current.next
                else:
                    previous.next = current.next

                self.length -= 1
                return

            previous = current
            current = current.next

        raise KeyError(f"Key '{key}' not found")

    def clear(self) -> None:
        self.hash_table = [None] * self.capacity
        self.length = 0

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Any) -> Any:
        value = self[key]
        self.__delitem__(key)

        return value

    def update(self, other: "Dictionary") -> None:
        for key in other:
            self[key] = other[key]

    def __iter__(self) -> Any:
        for node in self.hash_table:
            current = node

            while current is not None:
                yield current.key
                current = current.next
