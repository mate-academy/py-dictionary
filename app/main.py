class Dictionary:
    def __init__(
            self, initial_capacity: int = 8,
            load_factor: float = 0.75
    ) -> None:
        self.capacity = initial_capacity
        self.size = 0
        self.buckets = [None] * self.capacity
        self.load_factor = load_factor

    def __hash_key(self, key: any) -> int:
        return hash(key) % self.capacity

    def __resize(self) -> None:
        new_capacity: int = self.capacity * 2
        new_buckets: list[None | list[tuple]] = [None] * new_capacity
        for bucket in self.buckets:
            if bucket is not None:
                for key, value in bucket:
                    new_index: int = hash(key) % new_capacity
                    if new_buckets[new_index] is None:
                        new_buckets[new_index] = [(key, value)]
                    else:
                        new_buckets[new_index].append((key, value))
        self.buckets = new_buckets
        self.capacity = new_capacity

    def __setitem__(self, key: any, value: any) -> None:
        if self.size / self.capacity >= self.load_factor:
            self.__resize()
        index: int = self.__hash_key(key)
        if self.buckets[index] is None:
            self.buckets[index] = [(key, value)]
            self.size += 1
        else:
            for i, (k, v) in enumerate(self.buckets[index]):
                if k == key:
                    self.buckets[index][i] = (key, value)
                    return
            self.buckets[index].append((key, value))
            self.size += 1

    def __getitem__(self, key: any) -> any:
        index: int = self.__hash_key(key)
        if self.buckets[index] is None:
            raise KeyError(f"Key {key} not found.")
        for k, v in self.buckets[index]:
            if k == key:
                return v
        raise KeyError(f"Key {key} not found.")

    def __len__(self) -> int:
        return self.size

    def clear(self) -> None:
        self.buckets = [None] * self.capacity
        self.size = 0

    def __delitem__(self, key: any) -> None:
        index: int = self.__hash_key(key)
        if self.buckets[index] is None:
            raise KeyError(f"Key {key} not found.")
        for i, (k, v) in enumerate(self.buckets[index]):
            if k == key:
                del self.buckets[index][i]
                self.size -= 1
                if len(self.buckets[index]) == 0:
                    self.buckets[index] = None
                return
        raise KeyError(f"Key {key} not found.")

    def get(self, key: any, default: any = None) -> any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def pop(self, key: any, default: any = None) -> any:
        try:
            value: any = self.__getitem__(key)
            self.__delitem__(key)
            return value
        except KeyError:
            if default is not None:
                return default
            raise KeyError(f"Key {key} not found.")

    def update(self, other: any) -> None:
        if isinstance(other, Dictionary):
            for key in other:
                self[key] = other[key]
        elif isinstance(other, dict):
            for key, value in other.items():
                self[key] = value
        else:
            for key, value in other:
                self[key] = value

    def __iter__(self) -> any:
        for bucket in self.buckets:
            if bucket is not None:
                for key, value in bucket:
                    yield key
