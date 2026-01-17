# flake8: noqa

class Node:
    def __init__(self, key: object, value: object) -> None:
        self.key = key
        self.value = value
        self.hash = hash(key)


class Dictionary:
    def __init__(
            self,
            initial_capacity: int = 8,
            load_factor: float = 0.7) -> None:
        self.capacity = initial_capacity
        self.size = 0
        self.load_factor = load_factor
        self.table: list[Node | None] = [None] * self.capacity

    def __setitem__(self, key: object, value: object) -> None:
        if self.size / self.capacity >= self.load_factor:
            self._resize()

        index = self._find_slot(key, for_insert=True)
        if self.table[index] is None:
            self.size += 1
        self.table[index] = Node(key, value)

    def __getitem__(self, key: object) -> object:
        index = self._find_slot(key, for_insert=False)
        if index is None or self.table[index] is None:  # noqa: E713
            raise KeyError(f"Key '{key}' not found in CustomDictionary.")
        return self.table[index].value

    def __len__(self) -> int:
        return self.size

    def _find_slot(self, key: object, for_insert: bool) -> int | None:
        index = hash(key) % self.capacity
        start_index = index

        while self.table[index] is not None:
            if self.table[index].key == key:
                return index
            index = (index + 1) % self.capacity
            if index == start_index:
                return None if not for_insert else index

        return index if for_insert else None

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.size = 0
        self.table = [None] * self.capacity

        for node in old_table:
            if node is not None:
                self[node.key] = node.value
