class Dictionary:
    def __init__(self):
        self.capacity = 8
        self.length = 0
        self.load = int(self.capacity * 2 / 3)
        self.table = [[] for _ in range(self.capacity)]

    def __setitem__(self, key, value):
        hashed_key = hash(key)
        index = hashed_key % self.capacity
        while True:
            if self.table[index] == []:
                self.table[index] = [key, value, hashed_key]
                self.length += 1
                break
            if self.table[index][2] == hashed_key \
                    and self.table[index][0] == key:
                self.table[index][1] = value
                break
            index = (index + 1) % self.capacity
        if self.length == self.load:
            self.resize()

    def resize(self):
        self.capacity *= 2
        self.length = 0
        self.load = int(self.capacity * 2 / 3)
        old_table = self.table
        self.table = [[] for _ in range(self.capacity)]
        for element in old_table:
            if len(element):
                self.__setitem__(element[0], element[1])

    def __len__(self):
        return self.length

    def __getitem__(self, key):
        hashed_key = hash(key)
        index = hash(key) % self.capacity
        element = self.table[index]
        while element:
            if element[2] == hashed_key and element[0] == key:
                return element[1]
            index = (index + 1) % self.capacity
            element = self.table[index]
        raise KeyError(key)

    def clear(self):
        self.capacity = 8
        self.length = 0
        self.load = int(self.capacity * 2 / 3)
        self.table = [[] for _ in range(self.capacity)]

    def __delitem__(self, key):
        hashed_key = hash(key)
        index = hash(key) % self.capacity
        element = self.table[index]
        while element:
            if element[2] == hashed_key and element[0] == key:
                element[0] = None
                element[1] = None
                self.length -= 1
                break
            index = (index + 1) % self.capacity
            element = self.table[index]
        else:
            raise KeyError(key)

    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def pop(self, __key, default=None):
        try:
            item = self.__getitem__(__key)
            self.__delitem__(__key)
        except KeyError:
            if default:
                return default
            raise
        return item
