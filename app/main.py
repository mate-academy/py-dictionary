class Dictionary:
    def __init__(self):
        self.capacity = 8
        self.current_length = 0
        self.hash_table = [[] for _ in range(self.capacity)]

    def __setitem__(self, key, value):
        hash_ = hash(key)
        index = hash_ % self.capacity
        while self.hash_table[index]:
            if self.hash_table[index][1] == key:
                self.hash_table[index][2] = value
                self.current_length -= 1
                break
            else:
                index = (index + 1) % self.capacity
        self.hash_table[index] = [hash_, key, value]
        self.current_length += 1
        if int(self.capacity * (2 / 3)) < self.current_length:
            self.resize()

    def __getitem__(self, key):
        hash_ = hash(key)
        index = hash_ % self.capacity
        while self.hash_table[index]:
            if self.hash_table[index][1] == key:
                return self.hash_table[index][2]
            index = (index + 1) % self.capacity
        raise KeyError(f"Key: {key} not in dictionary!")

    def __len__(self):
        return self.current_length

    def resize(self):
        self.capacity *= 2
        hash_table_before = self.hash_table
        self.hash_table = [[] for _ in range(self.capacity)]
        self.current_length = 0
        for item in hash_table_before:
            if item:
                self.__setitem__(item[1], item[2])
