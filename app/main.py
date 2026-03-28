class Node:
    def __init__(self, key: object, value: object) -> None:
        self.key = key
        self.hash = hash(key)
        self.value = value


class Dictionary:
    def __init__(self, capacity: int = 8, load_factor: float = 2 / 3) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.size = 0
        self.buckets: list[list[Node]] = [[] for _ in range(self.capacity)]

    def _hash(self, key: object) -> int:
        return hash(key) % self.capacity

    def __len__(self) -> int:
        return self.size

    def __setitem__(self, key: object, value: object) -> None:
        index = self._hash(key)
        bucket = self.buckets[index]

        for node in bucket:
            if node.key == key:
                node.value = value
                return

        bucket.append(Node(key, value))
        self.size += 1

        if self.size / self.capacity > self.load_factor:
            self._resize()

    def __getitem__(self, key: object) -> object:
        index = self._hash(key)
        bucket = self.buckets[index]

        for node in bucket:
            if node.key == key:
                return node.value

        raise KeyError(f"Key '{key}' not found")

    def __delitem__(self, key: object) -> None:
        index = self._hash(key)
        bucket = self.buckets[index]

        for i, node in enumerate(bucket):
            if node.key == key:
                del bucket[i]
                self.size -= 1
                return

        raise KeyError(f"Key '{key}' not found")

    def clear(self) -> None:
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0

    def _resize(self) -> None:
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0

        for bucket in old_buckets:
            for node in bucket:
                self[node.key] = node.value
