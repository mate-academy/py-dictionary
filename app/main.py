class Node:
    def __init__(self, key: str, value: any) -> None:
        self.key = key
        self.hash = hash(key)
        self.value = value


class Dictionary:
    def __init__(self, initial_capacity: int = 8) -> None:
        self.capacity = initial_capacity
        self.size = 0
        self.table: list[list[Node] | None] = [None] * self.capacity

    def _hash(self, key: int) -> int:
        return hash(key) % self.capacity

    def __setitem__(self, key: int, value: int) -> None:
        index = self._hash(key)

        if self.table[index] is None:
            self.table[index] = [Node(key, value)]
            self.size += 1
        else:
            for node in self.table[index]:
                if node.key == key:
                    node.value = value
                    return
            self.table[index].append(Node(key, value))
            self.size += 1

        if self.size / self.capacity > 0.7:
            self._resize()

    def __getitem__(self, key: int) -> None:
        index = self._hash(key)
        if self.table[index] is None:
            raise KeyError(f"Key '{key}' not found")

        for node in self.table[index]:
            if node.key == key:
                return node.value

        raise KeyError(f"Key '{key}' not found")

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.size = 0
        self.table = [None] * self.capacity

        for bucket in old_table:
            if bucket:
                for node in bucket:
                    self.__setitem__(node.key, node.value)

    def __delitem__(self, key: int) -> None:
        index = self._hash(key)
        if self.table[index] is None:
            raise KeyError(f"Key '{key}' not found")

        for i, node in enumerate(self.table[index]):
            if node.key == key:
                del self.table[index][i]
                self.size -= 1
                return

        raise KeyError(f"Key '{key}' not found")
