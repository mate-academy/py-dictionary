class Dictionary:
    def __init__(self):
        self.capacity = 8
        self.threshold = int(self.capacity * (2 / 3))
        self.hash_table = [None for _ in range(self.capacity)]
        self.length = 0

    def __setitem__(self, key, value):
        if self.threshold == self.length:
            self.resize()
        if self.fill_hash_table(key, value, self.capacity, self.hash_table):
            self.length += 1

    def __getitem__(self, key):
        hash_ = hash(key)
        index_ = hash_ % self.capacity
        while self.hash_table[index_]:
            if self.hash_table[index_][1] == hash_ \
                    and self.hash_table[index_][0] == key:
                return self.hash_table[index_][2]
            index_ = (index_ + 1) % self.capacity
        raise KeyError(key)

    def __len__(self):
        return self.length

    @staticmethod
    def fill_hash_table(key, value, capacity, hash_table):
        len_flag = True
        hash_ = hash(key)
        index_ = hash_ % capacity
        while hash_table[index_]:
            if hash_table[index_][1] == hash_ and hash_table[index_][0] == key:
                len_flag = False
                break
            index_ = (index_ + 1) % capacity
        hash_table[index_] = (key, hash_, value)
        return len_flag

    def resize(self):
        self.capacity *= 2
        self.threshold = int(self.capacity * (2 / 3))
        tmp = [None for _ in range(self.capacity)]
        for node in self.hash_table:
            if node:
                self.fill_hash_table(node[0], node[2], self.capacity, tmp)
        self.hash_table = tmp

    def clear(self):
        self.hash_table = [None for _ in self.hash_table]
        self.length = 0

    def __delitem__(self, key):
        del_flag = True
        hash_ = hash(key)
        index_ = hash_ % self.capacity
        tmp = self.capacity if index_ == 0 else index_ - 1
        while tmp != index_:
            if self.hash_table[index_] \
                    and self.hash_table[index_][1] == hash_ \
                    and self.hash_table[index_][0] == key:
                self.hash_table[index_] = None
                self.length -= 1
                del_flag = False
                break
            index_ = (index_ + 1) % self.capacity
        if del_flag:
            raise KeyError(key)

    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def pop(self, key):
        try:
            value = self.get(key)
            self.__delitem__(key)
            return value
        except KeyError:
            raise

    def update(self, another_dict=None, **kwargs):
        if another_dict:
            for key, value in another_dict.items():
                self.__setitem__(key, value)
        for key, value in kwargs.items():
            self.__setitem__(key, value)

    def __iter__(self):
        for item in self.hash_table:
            if item:
                yield item[2]
