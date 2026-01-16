from typing import Any, Hashable, Optional


class Node:
    def __init__(self, key: Hashable, value: Any) -> None:
        self.key = key
        self.value = value
        self.next = None


class Dictionary:
    def __init__(self,
                 initial_capacity: int = 8,
                 load_factor: float = 2 / 3
                 ) -> None:
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.tables = [None] * self.capacity

    def get_index(self, key: Any) -> int:
        return hash(key) % self.capacity

    def _resize(self) -> None:
        new_table = self.tables
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.length = 0

        for trash in new_table:
            if trash is not None:
                for key, hashed_key, value in trash:
                    self[key] = value

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self.get_index(key)
        new_node = Node(key, value)

        if self.tables[index] is None:
            self.tables[index] = new_node
            self.size += 1
        else:
            current = self.tables[index]
            while current:
                if current.key == key:
                    current.value = value
                    return
                if current.next is None:
                    break
                current = current.next
            current.next = new_node
            self.size += 1

    def __getitem__(self, key: Hashable) -> Any:
        index = self.get_index(key)
        current = self.tables[index]

        while current:
            if current.key == key:
                return current.value
            current = current.next

        raise KeyError(f"Key '{key}' not found.")

    def __len__(self) -> int:
        return self.size

    def clear(self) -> None:
        self.tables = [[] for _ in range(self.capacity)]
        self.size = 0

    def __delitem__(self, key: Any) -> None:
        index = self.get_index(key)
        tables = self.tables[index]

        for element, node in enumerate(tables):
            if node.key == key:
                del tables[element]
                self.size -= 1
                return

        raise KeyError(f"Key '{key}' not found.")

    def get(self, key: Any, other: Optional[Any] = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return other

    def pop(self, key: Any, other: Optional[Any] = None) -> Any:
        index = self.get_index(key)
        tables = self.tables[index]

        for element, node in enumerate(tables):
            if node.key == key:
                value = node.value
                del tables[element]
                self.size -= 1
                return value

        if other is not None:
            return other

        raise KeyError(f"Key '{key}' not found.")

    def update(self, other: dict) -> None:
        for key, value in other.items():
            self[key] = value

    def __iter__(self) -> None:
        for table in self.tables:
            for node in table:
                yield node.key
