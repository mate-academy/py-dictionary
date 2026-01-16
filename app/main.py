from collections.abc import Hashable
from typing import Any, Optional


class Node:
    def __init__(self, key: Hashable, value: Any, hash_value: int) -> None:
        self.key = key
        self.value = value
        self.hash_value = hash_value
        self.next: Optional[Node] = None


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.load_factor_threshold = 2 / 3
        self.hash_table: list[Optional[Node]] = [None] * self.capacity

    def __len__(self) -> int:
        return self.length

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if (self.length + 1) / self.capacity > self.load_factor_threshold:
            self._resize()

        hash_value = hash(key)
        index = hash_value % self.capacity

        current = self.hash_table[index]
        prev = None
        while current:
            if current.hash_value == hash_value and current.key == key:
                current.value = value
                return
            prev = current
            current = current.next

        new_node = Node(key, value, hash_value)
        if prev:
            prev.next = new_node
        else:
            self.hash_table[index] = new_node
        self.length += 1

    def __getitem__(self, key: Hashable) -> Any:
        hash_value = hash(key)
        index = hash_value % self.capacity

        current = self.hash_table[index]
        while current:
            if current.hash_value == hash_value and current.key == key:
                return current.value
            current = current.next
        raise KeyError(f"Key '{key}' not found in dictionary.")

    def __delitem__(self, key: Hashable) -> None:
        hash_value = hash(key)
        index = hash_value % self.capacity

        current = self.hash_table[index]
        prev = None
        while current:
            if current.hash_value == hash_value and current.key == key:
                if prev:
                    prev.next = current.next
                else:
                    self.hash_table[index] = current.next
                self.length -= 1
                return
            prev = current
            current = current.next
        raise KeyError(f"Key '{key}' not found in dictionary.")

    def _resize(self) -> None:
        old_hash_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.length = 0

        for head_node in old_hash_table:
            current = head_node
            while current:
                self.__setitem__(current.key, current.value)
                current = current.next

    def __contains__(self, key: Hashable) -> bool:
        try:
            self.__getitem__(key)
            return True
        except KeyError:
            return False

    def __str__(self) -> str:
        items = []
        for i in range(self.capacity):
            current = self.hash_table[i]
            while current:
                items.append(f"{current.key}: {current.value}")
                current = current.next
        return "{" + ", ".join(items) + "}"

    def __repr__(self) -> str:
        return self.__str__()
