class Dictionary:
    def __init__(self):
        self.capacity = 8
        self.size = 0
        self.load_factor = 2 / 3
        self.hash_table = self.create_hash_table()

    def __setitem__(self, key, value):
        threshold = int(self.load_factor * self.capacity)
        if self.size == threshold:
            self.resize()
        hash_value = hash(key)
        self.form_hash_table(key, value, hash_value)

    def form_hash_table(self, key, value, hash_value):
        index = hash_value % self.capacity

        while True:
            if not self.hash_table[index]:
                self.size += 1
                self.hash_table[index] = [key, value, hash_value]
                break
            if self.hash_table[index][2] == hash_value \
                    and self.hash_table[index][0] == key:
                self.hash_table[index][1] = value
                break
            index = (index + 1) % self.capacity

    def __getitem__(self, key):
        hash_value = hash(key)
        index = hash_value % self.capacity

        while self.hash_table[index]:
            if self.hash_table[index][2] == hash_value \
                    and self.hash_table[index][0] == key:
                return self.hash_table[index][1]
            index = (index + 1) % self.capacity
        raise KeyError(key)

    def __len__(self):
        return self.size

    def resize(self):
        self.capacity *= 2
        copied_elements = self.hash_table.copy()
        self.hash_table = self.create_hash_table()
        self.size = 0
        for element in copied_elements:
            if element:
                self.__setitem__(element[0], element[1])

    def create_hash_table(self):
        return [[] for _ in range(self.capacity)]

    def clear(self):
        self.hash_table = self.create_hash_table()
        return self

    def __delitem__(self, key):
        for ind, val in enumerate(self.hash_table):
            if val:
                if val[0] == key and hash(key) == val[2]:
                    self.hash_table[ind] = []

    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def pop(self, key, default=None):
        for index, value in enumerate(self.hash_table):
            if value:
                if key == value[0] and hash(key) == value[2]:
                    self.hash_table[index] = []
                    return value[1]
        if default is not None:
            return default
        else:
            raise KeyError(key)

    def __iter__(self):
        self.current_element = 0
        return self

    def __next__(self):
        if self.current_element > self.__len__():
            raise StopIteration

        if not self.hash_table[self.current_element]:
            self.current_element += 1
        result = self.hash_table[self.current_element]
        self.current_element += 1
        return result
