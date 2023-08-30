class Dictionary:
    def __init__(self):
        self.length = 8
        self.size = 0
        self.hash_table = [[] for _ in range(self.length)]

    def __setitem__(self, key, value):
        hash_ = hash(key)
        index = hash_ % self.length
        while self.hash_table[index]:
            if self.hash_table[index][1] == key:
                self.hash_table[index][2] = value
                self.size -= 1
                break
            else:
                index = (index + 1) % self.length
        self.hash_table[index] = [hash_, key, value]
        self.size += 1
        if int(self.length * (2 / 3)) < self.size:
            self.resize()

    def __getitem__(self, key):
        hash_ = hash(key)
        index = hash_ % self.length
        while self.hash_table[index]:
            if self.hash_table[index][1] == key:
                return self.hash_table[index][2]
            index = (index + 1) % self.length
        raise KeyError(f"Key: {key} not in dictionary!")

    def resize(self):
        self.length *= 2
        hash_table_before = self.hash_table
        self.hash_table = [[] for _ in range(self.length)]
        self.size = 0
        for item in hash_table_before:
            if item:
                self.__setitem__(item[1], item[2])

    def __len__(self):
        return self.size
