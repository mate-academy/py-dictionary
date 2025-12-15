class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.hash = hash(key)

class Dictionary:
    def __init__(self, initial_capacity=8, load_factor=0.75):
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]

    def _hash(self, key):
        return hash(key) % self.capacity

    def _resize(self):
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0

        for bucket in old_buckets:
            for node in bucket:
                self[node.key] = node.value

    def __setitem__(self, key, value):
        if self.size / self.capacity > self.load_factor:
            self._resize()

        index = self._hash(key)
        bucket = self.buckets[index]

        for node in bucket:
            if node.key == key:
                node.value = value
                return

        bucket.append(Node(key, value))
        self.size += 1

    def __getitem__(self, key):
        index = self._hash(key)
        bucket = self.buckets[index]

        for node in bucket:
            if node.key == key:
                return node.value
        raise KeyError(key)

    def __len__(self):
        return self.size

    def __repr__(self):
        items = []
        for bucket in self.buckets:
            for node in bucket:
                items.append(f"{node.key!r}: {node.value!r}")
        return "{" + ", ".join(items) + "}"
