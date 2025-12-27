class Node:
    def __init__(self, key: str, value: str) -> None:
        self.key = key
        self.value = value
        self.hash = hash(key)


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.size = 0
        self.buckets = [[] for _ in range(capacity)]

    def _get_index(self, key_hash: int) -> int:
        return key_hash % self.capacity

    def __setitem__(self, key: str, value: str) -> None:
        key_hash = hash(key)
        index = self._get_index(key_hash)
        bucket = self.buckets[index]

        for node in bucket:
            if node.key == key:
                node.value = value
                return

        bucket.append(Node(key, value))
        self.size += 1

        if self.size / self.capacity > 0.75:
            self._resize()

    def __getitem__(self, key: str) -> str:
        key_hash = hash(key)
        index = self._get_index(key_hash)
        bucket = self.buckets[index]

        for node in bucket:
            if node.key == key:
                return node.value

        raise KeyError(f"Key {key} not found")

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0

        for bucket in old_buckets:
            for node in bucket:
                self[node.key] = node.value
