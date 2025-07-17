class Dictionary:
    class Node:
        def __init__(self, key: object, value: object) -> None:
            self.key: object = key
            self.value: object = value
            self.hash: int = hash(key)

    def __init__(self, initial_capacity: int = 8) -> None:
        self.capacity: int = initial_capacity
        self.length: int = 0
        self.load_factor: float = 0.7
        self.table: list = [None] * self.capacity

    def __setitem__(self, key: object, value: object) -> None:
        if self.length + 1 > self.capacity * self.load_factor:
            self._resize()
        index: int = self._index(key)
        while self.table[index] is not None:
            node = self.table[index]
            if node.key == key:
                node.value = value
                return
            index = (index + 1) % self.capacity
        self.table[index] = self.Node(key, value)
        self.length += 1

    def __getitem__(self, key: object) -> object:
        index: int = self._index(key)
        for _ in range(self.capacity):
            node = self.table[index]
            if node is None:
                raise KeyError(f"Key '{key}' not found.")
            if node.key == key:
                return node.value
            index = (index + 1) % self.capacity
        raise KeyError(f"Key '{key}' not found.")

    def __len__(self) -> int:
        return self.length

    def _index(self, key: object) -> int:
        return hash(key) % self.capacity

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.length = 0
        for node in old_table:
            if node is not None:
                self[node.key] = node.value

    def clear(self) -> None:
        self.table = [None] * self.capacity
        self.length = 0

    def __delitem__(self, key: object) -> None:
        index: int = self._index(key)
        for _ in range(self.capacity):
            node = self.table[index]
            if node is None:
                raise KeyError(f"Key '{key}' not found for deletion.")
            if node.key == key:
                self.table[index] = None
                self.length -= 1
                return
            index = (index + 1) % self.capacity
        raise KeyError(f"Key '{key}' not found for deletion.")

    def get(self, key: object, default: object = None) -> object:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: object) -> object:
        value: object = self[key]
        del self[key]
        return value

    def update(self, other: dict) -> None:
        for k, v in other.items():
            self[k] = v

    def __iter__(self) -> object:
        for node in self.table:
            if node is not None:
                yield node.key
