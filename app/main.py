from typing import Any


class Node:
    def __init__(self, key: Any, value: Any) -> Any:
        self.key = key
        self.value = value
        self.next = None


class Dictionary:
    def __init__(self,
                 initial_capacity: int = 8,
                 load_factor: float = 2 / 3
                 ) -> None:
        self._capacity = initial_capacity
        self._load_factor = round(self._capacity * load_factor)
        self._size = 0
        self._table = [None] * self._capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        hash_code = self._get_hash_code(key)
        index = hash_code % self._capacity

        new_node = Node(key, value)

        if self._table[index] is None:
            self._table[index] = new_node
        else:
            current = self._table[index]
            prev = None
            while current is not None:
                if current.key == key:
                    current.value = value
                    return
                prev = current
                current = current.next
            prev.next = new_node

        self._size += 1
        if self._size >= self._capacity * self._load_factor:
            self._resize_table()

    def __getitem__(self, key: Any) -> Any:
        hash_code = self._get_hash_code(key)
        index = hash_code % self._capacity

        current = self._table[index]
        while current is not None:
            if current.key == key:
                return current.value
            current = current.next

        raise KeyError(f"Key '{key}' not found.")

    def __len__(self) -> int:
        return self._size

    def __delitem__(self, key: Any) -> None:
        hash_code = self._get_hash_code(key)
        index = hash_code % self._capacity

        prev = None
        current = self._table[index]
        while current is not None:
            if current.key == key:
                if prev is None:
                    self._table[index] = current.next
                else:
                    prev.next = current.next
                self._size -= 1
                return
            prev = current
            current = current.next

        raise KeyError(f"Key '{key}' not found.")

    def _get_hash_code(self, key: Any) -> int:
        return hash(key)

    def _resize_table(self) -> None:
        new_capacity = self._capacity * 2
        new_table = [None] * new_capacity

        for i in range(self._capacity):
            current = self._table[i]
            while current is not None:
                new_index = current.key.__hash__() % new_capacity
                new_node = Node(current.key, current.value)

                if new_table[new_index] is None:
                    new_table[new_index] = new_node
                else:
                    temp: Node = new_table[new_index]
                    while temp.next is not None:
                        temp = temp.next
                    temp.next = new_node

                current = current.next

        self._table = new_table
        self._capacity = new_capacity

    def __repr__(self) -> str:
        items = []
        for i in range(self._capacity):
            current = self._table[i]
            while current is not None:
                items.append((current.key, current.value))
                current = current.next
        return f"Dictionary({', '.join([f'{k}: {v}' for k, v in items])})"
