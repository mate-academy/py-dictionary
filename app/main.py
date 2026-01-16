class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.size = 0
        self.hash_list = [[] for _ in range(self.capacity)]

    def _get_index(self, key: int) -> int:
        return hash(key) % self.capacity

    def __setitem__(self, key: int, value: int) -> None:
        index = self._get_index(key)
        bucket = self.hash_list[index]

        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))
        self.size += 1

        if self.size / self.capacity > 0.75:
            self._resize()

    def __getitem__(self, key: int) -> int:
        index = self._get_index(key)
        bucket = self.hash_list[index]

        for k, v in bucket:
            if k == key:
                return v
        raise KeyError(f"Key Element {key} not found.")

    def __delitem__(self, key: int) -> None:
        index = self._get_index(key)
        bucket = self.hash_list[index]

        for i, (k, _) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.size -= 1
                return
        raise KeyError(f"Key Element {key} not found.")

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        old_data = self.hash_list
        self.capacity *= 2
        self.hash_list = [[] for _ in range(self.capacity)]
        self.size = 0

        for bucket in old_data:
            for key, value in bucket:
                self[key] = value
