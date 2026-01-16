class Dictionary:
    class _Node:
        def __init__(self, key: object, value: object) -> None:
            self.key = key
            self.value = value
            self.hash = hash(key)

    def __init__(self, initial_capacity: int = 8) -> None:
        self._capacity = initial_capacity
        self._size = 0
        self._buckets = [None] * self._capacity
        self._load_factor = 0.75

    def _resize(self) -> None:
        old_buckets = self._buckets
        self._capacity *= 2
        self._buckets = [None] * self._capacity
        self._size = 0

        for node in old_buckets:
            if node is not None:
                self[node.key] = node.value

    def _probe(self, key: object) -> int:
        index = hash(key) % self._capacity
        start_index = index

        while self._buckets[index] is not None:
            if self._buckets[index].key == key:
                return index
            index = (index + 1) % self._capacity
            if index == start_index:
                raise Exception(f"Hash table is full. Could not insert key: {key}")
        return index

    def __setitem__(self, key: object, value: object) -> None:
        if self._size / self._capacity > self._load_factor:
            self._resize()

        index = hash(key) % self._capacity
        while self._buckets[index] is not None:
            if self._buckets[index].key == key:
                self._buckets[index].value = value
                return
            index = (index + 1) % self._capacity

        self._buckets[index] = self._Node(key, value)
        self._size += 1

    def __getitem__(self, key: object) -> object:
        index = hash(key) % self._capacity
        start_index = index

        while self._buckets[index] is not None:
            if self._buckets[index].key == key:
                return self._buckets[index].value
            index = (index + 1) % self._capacity
            if index == start_index:
                break
        raise KeyError(key)

    def __len__(self) -> int:
        return self._size
