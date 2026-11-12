from __future__ import annotations


class Node:
    def __init__(self, key: object, hash_value: int, value: object) -> None:
        self.key = key
        self.hash = hash_value
        self.value = value


class Dictionary:
    def __init__(
        self,
        capacity: int = 8,
        load_factor: float = 0.75,
    ) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.size = 0
        self.hash_table: list[Node | None] = [None] * capacity

    def __setitem__(self, key: object, value: object) -> None:
        hash_value = hash(key)
        index = hash_value % self.capacity

        while True:
            node = self.hash_table[index]

            if node is None:
                self.hash_table[index] = Node(key, hash_value, value)
                self.size += 1

                if self.size / self.capacity > self.load_factor:
                    self._resize()

                return

            if node.hash == hash_value and node.key == key:
                node.value = value
                return

            index = (index + 1) % self.capacity

    def __getitem__(self, key: object) -> object:
        hash_value = hash(key)
        index = hash_value % self.capacity

        while True:
            node = self.hash_table[index]

            if node is None:
                raise KeyError(key)

            if node.hash == hash_value and node.key == key:
                return node.value

            index = (index + 1) % self.capacity

    def __len__(self) -> int:
        return self.size

    def __contains__(self, key: object) -> bool:
        try:
            self.__getitem__(key)
        except KeyError:
            return False

        return True

    def __iter__(self):
        for node in self.hash_table:
            if node is not None:
                yield node.key

    def __delitem__(self, key: object) -> None:
        hash_value = hash(key)
        index = hash_value % self.capacity

        while True:
            node = self.hash_table[index]

            if node is None:
                raise KeyError(key)

            if node.hash == hash_value and node.key == key:
                self.hash_table[index] = None
                self.size -= 1
                self._rehash_cluster((index + 1) % self.capacity)
                return

            index = (index + 1) % self.capacity

    def _rehash_cluster(self, index: int) -> None:
        while self.hash_table[index] is not None:
            node = self.hash_table[index]
            self.hash_table[index] = None
            self.size -= 1
            self[node.key] = node.value
            index = (index + 1) % self.capacity

    def get(self, key: object, default: object = None) -> object:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def pop(self, key: object, *args: object) -> object:
        if len(args) > 1:
            raise TypeError(
                "pop expected at most 2 arguments, got "
                f"{len(args) + 1}"
            )

        try:
            value = self.__getitem__(key)
            self.__delitem__(key)
        except KeyError:
            if args:
                return args[0]

            raise

        return value

    def update(self, other: object) -> None:
        if isinstance(other, Dictionary):
            for key in other:
                self[key] = other[key]

            return

        for key, value in other:
            self[key] = value

    def clear(self) -> None:
        self.capacity = 8
        self.load_factor = 0.75
        self.size = 0
        self.hash_table = [None] * self.capacity

    def _resize(self) -> None:
        old_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.size = 0

        for node in old_table:
            if node is not None:
                self[node.key] = node.value
