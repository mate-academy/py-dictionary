class Dictionary:

    def __init__(self):
        self.capacity = 8
        self.length = 0
        self.threshold = int(self.capacity * 2 / 3)
        self.table_hash = [[] for _ in range(self.capacity)]

    def __setitem__(self, key, value):
        key_hash = hash(key)
        index = key_hash % self.capacity
        while True:
            if len(self.table_hash[index]) == 0:
                self.table_hash[index] = [key, value, key_hash]
                self.length += 1
                break
            if self.table_hash[index][0] == key and \
                    self.table_hash[index][2] == key_hash:
                self.table_hash[index][1] = value
                break
            index = (index + 1) % self.capacity
        if self.length == self.threshold:
            self.resize()

    def resize(self):
        self.capacity *= 2
        self.length = 0
        self.threshold = int(self.capacity * 2 / 3)
        old_table_hash = self.table_hash
        self.table_hash = [[] for _ in range(self.capacity)]
        for cell in old_table_hash:
            if len(cell) != 0:
                self.__setitem__(cell[0], cell[1])

    def __getitem__(self, key):
        index = hash(key) % self.capacity
        cell = self.table_hash[index]
        while True:
            try:
                if cell[0] == key and cell[2] == hash(key):
                    return cell[1]
            except IndexError:
                raise KeyError
            index = (index + 1) % self.capacity
            cell = self.table_hash[index]

    def __len__(self):
        return self.length
