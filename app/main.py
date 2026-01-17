from typing import Any, Hashable


class Node:
    def __init__(self, key: Hashable, value: Any) -> None:
        self.key = key
        self.value = value
        self.hash = hash(key)


class Dictionary:
    def __init__(self, load_factor: float = 2 / 3) -> None:
        self.hash_table = [None] * 8
        self.load_factor = load_factor
        self.size = 0  # Track the number of stored items

    def __setitem__(self, key: Hashable, value: Any) -> None:
        self._resize()
        new_node = Node(key, value)
        cell = self.get_slot(key)

        # Linear probing to find the correct slot
        while self.hash_table[cell] is not None and \
                self.hash_table[cell].key != key:
            cell = (cell + 1) % len(self.hash_table)  # Move to the next slot

        if self.hash_table[cell] is None:
            self.size += 1  # Increment count only for new insertions

        self.hash_table[cell] = new_node

    def __getitem__(self, key: Hashable) -> Any:
        cell = self.get_slot(key)

        # Linear probing for lookup
        start = cell
        while self.hash_table[cell] is not None:
            if self.hash_table[cell].key == key:
                return self.hash_table[cell].value
            cell = (cell + 1) % len(self.hash_table)
            if cell == start:  # Prevent infinite loop
                break

        raise KeyError(f"Key {key} not found")

    def _resize(self) -> None:
        if self.size >= len(self.hash_table) * self.load_factor:
            old_hash_table = self.hash_table
            self.hash_table = [None] * (len(self.hash_table) * 2)
            self.size = 0  # Reset size

            for node in old_hash_table:
                if node:
                    self.__setitem__(node.key, node.value)

    def get_slot(self, key: Hashable) -> int:
        return hash(key) % len(self.hash_table)

    def __len__(self) -> int:
        return self.size
