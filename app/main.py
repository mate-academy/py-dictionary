from typing import Any


class Dictionary:
    def __init__(self, capacity: int = 8, load_factor: float = 0.75) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.table = [None] * self.capacity
        self.size = 0

    def __setitem__(self, key: int, value: Any) -> None:
        h = hash(key)
        index = h % self.capacity
        node = Node(key, h, value)
        bucket = self.table[index]

        if bucket is None:
            self.table[index] = [node]
            self.size += 1
            return

        for existing_node in bucket:
            if existing_node.key == key:
                existing_node.value = value
                return

        self.table[index].append(node)
        self.size += 1

    def __getitem__(self, key: int) -> Any:
        h = hash(key)
        index = h % self.capacity
        bucket = self.table[index]

        if bucket is None:
            raise KeyError

        for existing_node in bucket:
            if existing_node.key == key:
                return existing_node.value
        raise KeyError

    def __len__(self) -> int:
        return self.size

    def resize(self) -> None:
        old_table = self.table
        if (self.size / self.capacity) > self.load_factor:
            new_capacity = self.capacity * 2
            self.capacity = new_capacity
            self.table = [None] * self.capacity
            self.size = 0

            for bucket in old_table:
                if bucket is None:
                    continue
                for node in bucket:
                    self.__setitem__(node.key, node.value)


class Node:
    def __init__(self, key: int, h: int, value: Any) -> None:
        self.key = key
        self.h = h
        self.value = value
