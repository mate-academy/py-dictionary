class Dictionary:
    def __init__(self):
        self.capacity = 8
        self.threshold = int(self.capacity * 2 / 3)
        self.length = 0
        self.hash_table = [[] for _ in range(self.capacity)]

    def __setitem__(self, key, value):
        hash_key = hash(key)
        index = hash_key % self.capacity
        while True:
            if len(self.hash_table[index]) == 0:
                self.hash_table[index] = [key, value, hash_key]
                self.length += 1
                break
            if self.hash_table[index][0] == key and \
                    self.hash_table[index][2] == hash_key:
                self.hash_table[index][1] = value
                break
            index = (index + 1) % self.capacity
        if self.length == self.threshold:
            self.resize()

    def resize(self):
        self.capacity *= 2
        self.length = 0
        self.threshold = int(self.capacity * 2 / 3)
        old_hash_table = self.hash_table
        self.hash_table = [[] for _ in range(self.capacity)]
        for cell in old_hash_table:
            if len(cell) != 0:
                self.__setitem__(cell[0], cell[1])

    def __getitem__(self, key):
        index = hash(key) % self.capacity
        cell = self.hash_table[index]
        while True:
            try:
                if cell[0] == key and cell[2] == hash(key):
                    return cell[1]
            except IndexError as e:
                raise KeyError from e
            index = (index + 1) % self.capacity
            cell = self.hash_table[index]

    def __len__(self):
        return self.length

    def clear(self):
        self.hash_table.clear()

    def get(self, key):
        return self.__getitem__(key)
