class Node:
    def __init__(self, key: object, value: object) -> None:
        self.key: object = key
        self.hash: int = hash(key)
        self.value: object = value


class Dictionary:
    INITIAL_CAPACITY: int = 8
    LOAD_FACTOR: float = 2 / 3

    def __init__(self) -> None:
        self.capacity: int = self.INITIAL_CAPACITY
        self.table: list[Node | None] = [None] * self.capacity
        self.size: int = 0

    def __setitem__(self, key: object, value: object) -> None:
        if (self.size + 1) > self.capacity * self.LOAD_FACTOR:
            self._resize()

        hash_code: int = hash(key)
        index: int = hash_code % self.capacity

        while self.table[index] is not None:
            node: Node = self.table[index]

            if node.hash == hash_code and node.key == key:
                node.value = value
                return

            index = (index + 1) % self.capacity

        self.table[index] = Node(key, value)
        self.size += 1

    def __getitem__(self, key: object) -> object:
        hash_code: int = hash(key)
        index: int = hash_code % self.capacity

        while self.table[index] is not None:
            node: Node = self.table[index]

            if node.hash == hash_code and node.key == key:
                return node.value

            index = (index + 1) % self.capacity

        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        old_table: list[Node | None] = self.table

        self.capacity = int(self.capacity * 1.5) + 8
        self.table = [None] * self.capacity
        self.size = 0

        for node in old_table:
            if node is not None:
                self[node.key] = node.value
