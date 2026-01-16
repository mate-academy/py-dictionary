class Dictionary:
    def __init__(self):
        self.capacity = 8
        self.length = 0
        self.threshold = int(self.capacity * 2 / 3)
        self.hash_table = [None for _ in range(self.capacity)]

    def __setitem__(self, key, value):
        if self.length == self.threshold:
            self.resize()
        hash_ = hash(key)
        index_ = hash_ % self.capacity
        while True:
            if not self.hash_table[index_]:
                self.hash_table[index_] = [key, hash_, value]
                self.length += 1
                break
            if self.hash_table[index_][0] == key and \
                    self.hash_table[index_][1] == hash_:
                self.hash_table[index_][2] = value
                break
            index_ = (index_ + 1) % self.capacity

    def __getitem__(self, key):
        hash_ = hash(key)
        index_ = hash_ % self.capacity
        while self.hash_table[index_]:
            if self.hash_table[index_][0] == key and \
                    self.hash_table[index_][1] == hash_:
                return self.hash_table[index_][2]
            index_ = (index_ + 1) % self.capacity
        raise KeyError(key)

    def __len__(self):
        return self.length

    def resize(self):
        self.capacity *= 2
        self.length = 0
        self.threshold = int(self.capacity * 2 / 3)
        temp_hash_table = self.hash_table.copy()
        self.hash_table = [None for _ in range(self.capacity)]
        for item in temp_hash_table:
            if item is not None:
                self.__setitem__(item[0], item[2])

    def clear(self):
        self.length = 0
        self.capacity = 8
        self.hash_table = [None for _ in range(self.capacity)]

    def get(self, key, value: None):
        try:
            return self.__getitem__(key)
        except KeyError:
            return value
