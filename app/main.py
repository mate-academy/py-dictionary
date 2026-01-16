class Dictionary:
    class Node:
        def __init__(self, key, value):
            self.key = key
            self.hash = hash(key)
            self.value = value

        def __eq__(self, other):
            return self.hash == other.hash and self.key == other.key

    def __init__(self, initial_capacity=8, load_factor=0.75):
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]

    def __len__(self):
        return self.size

    def __setitem__(self, key, value):
        if self.size / self.capacity > self.load_factor:
            self._resize()

        node = self.Node(key, value)
        index = node.hash % self.capacity
        bucket = self.buckets[index]

        for i, existing_node in enumerate(bucket):
            if existing_node.key == key:
                bucket[i] = node
                return

        bucket.append(node)
        self.size += 1

    def __getitem__(self, key):
        h = hash(key)
        index = h % self.capacity
        bucket = self.buckets[index]

        for node in bucket:
            if node.key == key:
                return node.value

        raise KeyError(f"Key {key} not found.")

    def _resize(self):
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        # Do NOT reset self.size here — we’ll manually rebuild

        for bucket in old_buckets:
            for node in bucket:
                index = node.hash % self.capacity
                self.buckets[index].append(node)
