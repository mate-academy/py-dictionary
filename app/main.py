from typing import Any, Iterator


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.value = value
        self.hash_of = hash(key)


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.size = 0
        self.table = [None] * capacity

    def _table_resize(self) -> None:
        new_capacity = self.capacity * 2
        new_table = [None] * new_capacity

        for bucket in self.table:
            if bucket:
                for node in bucket:
                    index = node.hash_of % new_capacity
                    if new_table[index] is None:
                        new_table[index] = []
                    new_table[index].append(node)

        self.table = new_table
        self.capacity = new_capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.size / self.capacity > 2 / 3:
            self._table_resize()

        index = hash(key) % self.capacity
        if self.table[index] is None:
            self.table[index] = []

        for node in self.table[index]:
            if node.key == key:
                node.value = value
                return

        self.table[index].append(Node(key, value))
        self.size += 1

    def __getitem__(self, key: Any) -> Any:
        index = hash(key) % self.capacity

        if self.table[index] is not None:
            for node in self.table[index]:
                if node.key == key:
                    return node.value
        raise KeyError(f"Can not get item by this key. Key {key} not found.")

    def __len__(self) -> int:
        return self.size

    def clear(self) -> None:
        for i in range(len(self.table)):
            if self.table[i] is not None:
                self.table[i] = None
        self.size = 0

    def __delitem__(self, key: Any) -> None:
        index = hash(key) % self.capacity
        if self.table[index] is not None:
            bucket = self.table[index]
            for i, node in enumerate(bucket):
                if node.key == key:
                    bucket.pop(i)
                    self.size -= 1
                    if not bucket:
                        self.table[index] = None
                    return
        raise KeyError(f"Can not delete item by this key. Key {key} not found")

    def get(self, key: Any, default: Any = None) -> Any:
        index = hash(key) % self.capacity

        if self.table[index] is not None:
            for node in self.table[index]:
                if node.key == key:
                    return node.value
        return default

    def pop(self, key: Any, default: Any = None) -> Any:
        index = hash(key) % self.capacity
        if self.table[index] is not None:
            bucket = self.table[index]
            for i, node in enumerate(bucket):
                if node.key == key:
                    item = node.value
                    bucket.pop(i)
                    self.size -= 1
                    if not bucket:
                        self.table[index] = None
                    return item
        if default is not None:
            return default
        raise KeyError(f"Can not pop item by this key. Key {key} not found")

    def update(self, other_dict: Any) -> None:
        if isinstance(other_dict, dict):
            for key, value in other_dict.items():
                self.__setitem__(key, value)
        elif isinstance(other_dict, Dictionary):
            for key in other_dict:
                self[key] = other_dict[key]
        else:
            for key, value in other_dict:
                self[key] = value

    def __iter__(self) -> Iterator[Any]:
        for bucket in self.table:
            if bucket:
                for node in bucket:
                    yield node.key
