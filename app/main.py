class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.length = 0
        self.hash_table: list = [None] * self.capacity

    def __setitem__(self, key: str, value: str) -> None:
        if self.length >= self.capacity * 2 // 3:
            self.resize()
        hash_ = hash(key)
        index = hash_ % self.capacity
        while True:
            if self.hash_table[index] is None:
                self.hash_table[index] = [key, value, hash_]
                self.length += 1
            if self.hash_table[index][2] == hash_ and \
                    self.hash_table[index][0] == key:
                self.hash_table[index][1] = value
                break
            index = (index + 1) % self.capacity

    def resize(self) -> None:
        self.capacity *= 2
        new_dict_data = self.hash_table
        self.hash_table = [None] * self.capacity
        self.length = 0
        for elem in new_dict_data:
            if elem:
                self.__setitem__(elem[0], elem[1])

    def __getitem__(self, key: str) -> str:
        hash_ = hash(key)
        index = hash_ % self.capacity
        while self.hash_table[index] is not None:
            if self.hash_table[index][2] == hash_ and \
                    self.hash_table[index][0] == key:
                return self.hash_table[index][1]
            index = (index + 1) % self.capacity
        raise KeyError

    def __len__(self) -> int:
        return self.length
