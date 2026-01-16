class Dictionary:
    def __init__(self, initial_capacity: int = 8) -> None:
        self.capacity: int = initial_capacity
        self.size: int = 0
        self.table: list[list[tuple[object, object]]] = [
            [] for _ in range(self.capacity)
        ]
        self.load_factor: float = 0.75

    def _hash(self, key: object) -> int:
        return hash(key) % self.capacity

    def __setitem__(self, key: object, value: object) -> None:
        index = self._hash(key)
        bucket = self.table[index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))
        self.size += 1

        if self.size / self.capacity >= self.load_factor:
            self._resize()

    def __getitem__(self, key: object) -> object:
        index = self._hash(key)
        bucket = self.table[index]

        for k, v in bucket:
            if k == key:
                return v

        raise KeyError(f"Key {key} not found in dictionary")

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        new_capacity: int = self.capacity * 2
        new_table: list[list[tuple[object, object]]] = [[] for _ in range(
            new_capacity)
        ]

        for bucket in self.table:
            for key, value in bucket:
                new_index = hash(key) % new_capacity
                new_table[new_index].append((key, value))

        self.capacity = new_capacity
        self.table = new_table
