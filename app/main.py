class Dictionary:
    def __init__(self):
        self.ls = [None] * 8
        self.capacity = 8
        self.size = 0

    def __setitem__(self, key, value):
        if self.size == int(self.capacity * 2 / 3):
            self.resize()
        self.add_element(key, value)

    def add_element(self, key, value):
        key_hash = hash(key)
        index = key_hash % self.capacity
        if self.ls[index] is not None:
            while True:
                if index == self.capacity:
                    index = 0
                if self.ls[index] is None:
                    self.ls[index] = (key, value, key_hash)
                    self.size += 1
                    break
                if self.ls[index][0] == key:
                    self.ls[index] = (key, value, key_hash)
                    break
                index += 1
        else:
            self.ls[index] = (key, value, key_hash)
            self.size += 1

    def resize(self):
        self.capacity *= 2
        copied_ls = self.ls.copy()
        self.ls = [None] * self.capacity
        self.size = 0
        for cell in copied_ls:
            if cell is not None:
                self.add_element(cell[0], cell[1])

    def __getitem__(self, key):
        key_hash = hash(key)
        index = key_hash % self.capacity

        while self.ls[index] is not None:
            if index == self.capacity:
                index = 0
            if self.ls[index][2] == key_hash and self.ls[index][0] == key:
                return self.ls[index][1]
            index = (index + 1) % self.capacity

        raise KeyError("No value with such key in this dict.")

    def __len__(self):
        return self.size

    def clear(self):
        for index, element in enumerate(self.ls):
            if element is not None:
                self.ls[index] = None
        self.size = 0

    def __delitem__(self, key):
        key_hash = hash(key)
        index = key_hash % self.capacity

        while self.ls[index] is not None:
            if index == self.capacity:
                index = 0
            if self.ls[index][2] == key_hash and self.ls[index][0] == key:
                self.ls[index] = None
                self.size -= 1
            index = (index + 1) % self.capacity

        raise KeyError("No value with such key in this dict.")

    def get(self, key, default=None):
        key_hash = hash(key)
        index = key_hash % self.capacity

        while self.ls[index] is not None:
            if index == self.capacity:
                index = 0
            if self.ls[index][2] == key_hash and self.ls[index][0] == key:
                return self.ls[index][1]
            index = (index + 1) % self.capacity

        return default

    def pop(self, key):
        key_hash = hash(key)
        index = key_hash % self.capacity

        while self.ls[index] is not None:
            if self.ls[index][2] == key_hash and self.ls[index][0] == key:
                pop = self.ls[index][1]
                self.ls[index] = None
                self.size -= 1
                return pop
            index = (index + 1) % self.capacity

        raise KeyError("No value with such key in this dict.")

    def update(self, dictionary):
        for key, value in dictionary.items():
            self.__setitem__(key, value)

    def __repr__(self):
        return str(self.ls)
