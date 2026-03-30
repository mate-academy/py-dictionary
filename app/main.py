class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.dictionary = [None] * self.capacity
        self.size = 0

    def __setitem__(self, key, value) -> None:
        load_factor = self.size / self.capacity
        if load_factor > (2 / 3):
            self._resize()

        h = hash(key)
        index = h % self.capacity
        if self.dictionary[index] is None:
            self.dictionary[index] = []
        for i, (k, stored_hash, v) in enumerate(self.dictionary[index]):
            if k == key and stored_hash == h:
                self.dictionary[index][i] = (key, h, value)
                return
        self.dictionary[index].append((key, h, value))
        self.size += 1

    def __getitem__(self, key) -> None:
        h = hash(key)
        index = h % self.capacity
        if self.dictionary[index] is None:
            raise KeyError(f"Key {key} is not in the dictionary")
        for i, (k, stored_hash, v) in enumerate(self.dictionary[index]):
            if k == key and stored_hash == h:
                return v
        raise KeyError(f"Key {key} is not in the dictionary")

    def _resize(self) -> None:
        old = self.dictionary
        self.capacity *= 2
        self.dictionary = [None] * self.capacity
        self.size = 0
        for slot in old:
            if slot:
                for key, h, value in slot:
                    self[key] = value

    def __len__(self) -> int:
        return self.size
