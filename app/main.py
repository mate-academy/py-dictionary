from typing import Hashable, Any


class Dictionary:
    def __init__(
            self,
            initial_capacity: int = 8,
            load_factor: float = 0.75
    ) -> None:

        self.initial_capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.table = [None] * initial_capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:

        hash_val = hash(key)
        index = hash_val % len(self.table)
        node = self.table[index]

        while node is not None:
            if node[0] == key:
                node[2] = value
                return
            node = node[1]

        self.table[index] = [key, self.table[index], value]
        self.size += 1

        if self.size >= self.load_factor * len(self.table):
            self.resize()

    def __getitem__(self, key: Hashable) -> Any:

        hash_val = hash(key)
        index = hash_val % len(self.table)
        node = self.table[index]

        while node is not None:
            if node[0] == key:
                return node[2]
            node = node[1]

        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def resize(self) -> None:

        new_capacity = len(self.table) * 2
        new_table = [None] * new_capacity

        for node in self.table:
            while node is not None:
                key, next_node, value = node
                index = hash(key) % new_capacity
                new_table[index] = [key, new_table[index], value]
                node = next_node

        self.initial_capacity = new_capacity
        self.table = new_table

    def __delitem__(self, key: Hashable) -> None:

        hash_val = hash(key)
        index = hash_val % len(self.table)
        node = self.table[index]
        prev_node = None

        while node is not None:
            if node[0] == key:
                if prev_node is None:
                    self.table[index] = node[1]
                else:
                    prev_node[1] = node[1]
                self.size -= 1
                return
            prev_node = node
            node = node[1]

        raise KeyError(key)

    def clear(self) -> None:

        self.table = [None] * self.initial_capacity
        self.size = 0

    def get(self, key: Hashable, default: Any = None) -> Any:

        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Hashable, default: Any = None) -> Any:

        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            return default

    def update(self, other_dict: Any) -> Any:

        for key, value in other_dict.items():
            self[key] = value

    def __iter__(self) -> None:

        for node in self.table:
            while node is not None:
                yield node[0]
                node = node[1]
