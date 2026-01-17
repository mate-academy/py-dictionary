class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.size = 0
        self.table = [None] * self.capacity
        self.load_factor = 2 / 3

    def _resize(self) -> None:
        self.capacity *= 2
        old_table = self.table
        self.size = 0
        self.table = [None] * self.capacity

        for item in old_table:
            if item:
                self.__setitem__(item["key"], item["value"])

    def __setitem__(self, key: any, value: any) -> None:
        key_hash = hash(key)
        index = key_hash % self.capacity

        while self.table[index] and self.table[index]["key"] != key:
            index = (index + 1) % self.capacity
        if not self.table[index]:
            self.size += 1
        self.table[index] = {
            "key": key,
            "hash": key_hash,
            "value": value,
        }

        if self.size > self.capacity * self.load_factor:
            self._resize()

    def __getitem__(self, key: any) -> any:
        key_hash = hash(key)
        index = key_hash % self.capacity

        while self.table[index]:
            if self.table[index]["key"] == key:
                return self.table[index]["value"]
            index = (index + 1) % self.capacity

        raise KeyError(f"Key '{key}' not found.")

    def __len__(self) -> int:
        return self.size
