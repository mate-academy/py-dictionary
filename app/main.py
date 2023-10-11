class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.hash_table = [None] * self.capacity
        self.lens = 0
        self.load_factor = 2.3

    def __setitem__(self, key: int, value: int) -> None:
        hash_key = hash(key)
        dicts_index = hash_key % self.capacity
        if self.lens >= self.capacity // self.load_factor:
            self.resize()
            dicts_index = hash_key % self.capacity

        while True:
            if self.hash_table[dicts_index] is None:
                self.hash_table[dicts_index] = [key, hash_key, value]
                self.lens += 1
                break
            elif self.hash_table[dicts_index][0] == key:
                self.hash_table[dicts_index][2] = value
                break
            dicts_index = (dicts_index + 1) % self.capacity

    def __getitem__(self, key: int) -> int:
        hash_key = hash(key)
        dicts_index = hash_key % self.capacity
        while True:
            if self.hash_table[dicts_index] is None:
                raise KeyError(f"{key} not found")
            elif self.hash_table[dicts_index][0] == key and (
                    self.hash_table[dicts_index][1] == hash_key):
                return self.hash_table[dicts_index][2]
            dicts_index = (dicts_index + 1) % self.capacity

    def __len__(self) -> int:
        return self.lens

    def resize(self) -> None:
        new_capacity = self.capacity * 2
        old_table = self.hash_table
        self.hash_table = [None] * new_capacity
        self.capacity = new_capacity
        self.lens = 0
        for item in old_table:
            if item:
                self.__setitem__(item[0], item[2])
