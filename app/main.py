class Dictionary:
    def __init__(self):
        self.capacity = 8
        self.length = 0
        self.hash_table = [[] for _ in range(self.capacity)]

    def __setitem__(self, key, value):
        key_hash = hash(key)
        index = key_hash % self.capacity
        while self.hash_table[index]:
            if self.hash_table[index][0] == key_hash and\
                    self.hash_table[index][1] == key:
                self.hash_table[index][2] = value
                self.length -= 1
                break
            else:
                index = (index + 1) % self.capacity
        self.hash_table[index] = [key_hash, key, value]
        self.length += 1
        if int(self.capacity * (2 / 3)) < self.length:
            self.resize()

    def __getitem__(self, key):
        key_hash = hash(key)
        index = key_hash % self.capacity
        while self.hash_table[index]:
            if self.hash_table[index][0] == key_hash and \
                    self.hash_table[index][1] == key:
                return self.hash_table[index][2]
            index = (index + 1) % self.capacity
        raise KeyError

    def __len__(self):
        return self.length

    def resize(self):
        self.capacity *= 2
        old_hash_table = self.hash_table
        self.hash_table = [[] for _ in range(self.capacity)]
        self.length = 0
        for element in old_hash_table:
            if element:
                self.__setitem__(element[1], element[2])
