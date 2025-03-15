class Dictionary:
    def __init__(self, initial_capacity: int = 8) -> None:
        self.capacity: int = initial_capacity
        self.size: int = 0
        self.buckets: list[list[list]] = [[] for _ in range(self.capacity)]

    def _hash(self, key: object) -> int:
        return hash(key) % self.capacity

    def __setitem__(self, key: object, value: object) -> None:
        index: int = self._hash(key)

        for pair in self.buckets[index]:
            if pair[0] == key:
                pair[1] = value
                return

        self.buckets[index].append([key, value])
        self.size += 1

        if self.size / self.capacity > 0.7:
            self._resize()

    def __getitem__(self, key: object) -> object:
        index: int = self._hash(key)

        for pair in self.buckets[index]:
            if pair[0] == key:
                return pair[1]

        raise KeyError(f'Ключ "{key}" не найден в словаре')

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        old_buckets: list[list[list]] = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0

        for bucket in old_buckets:
            for key, value in bucket:
                index = self._hash(key)
                if not any(pair[0] == key for pair in self.buckets[index]):
                    self.buckets[index].append([key, value])
                    self.size += 1
