class Node:
    def __init__(self, key: object, value: object) -> None:
        self.key: object = key
        self.value: object = value
        self.hash: int = hash(key)
        self.next: "Node | None" = None


class Dictionary:
    def __init__(self, initial_capacity: int = 8) -> None:
        self.capacity: int = initial_capacity
        self.size: int = 0
        self.buckets: list["Node | None"] = [None] * self.capacity

    def _index(self, key_hash: int) -> int:
        return key_hash % self.capacity

    def _resize(self) -> None:
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [None] * self.capacity
        self.size = 0

        node: "Node | None"
        for node in old_buckets:
            while node is not None:
                self[node.key] = node.value
                node = node.next

    def __setitem__(self, key: object, value: object) -> None:
        if self.size / self.capacity > 0.7:
            self._resize()

        key_hash = hash(key)
        index = self._index(key_hash)

        node = self.buckets[index]

        if node is None:
            self.buckets[index] = Node(key, value)
            self.size += 1
            return

        prev: "Node | None" = None
        while node is not None:
            if node.key == key:
                node.value = value
                return
            prev = node
            node = node.next

        prev.next = Node(key, value)
        self.size += 1

    def __getitem__(self, key: object) -> object:
        key_hash = hash(key)
        index = self._index(key_hash)

        node = self.buckets[index]
        while node is not None:
            if node.key == key:
                return node.value
            node = node.next

        raise KeyError(f"Key '{key}' not found")

    def __len__(self) -> int:
        return self.size
