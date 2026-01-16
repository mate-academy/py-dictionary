class Dictionary:
    def __init__(self):
        self.__size = 0
        self.hash_table = [None] * 8
        self.capacity = 8
        self.limit_to_resize = self.capacity * 2 / 3

    def get_need_index(self, ind, key, hash_key):
        if self.hash_table[ind] is None:
            return ind
        if self.hash_table[ind][0] == key:
            return ind

        while True:
            if not self.hash_table[ind]:
                return ind
            if self.hash_table[ind][0] == key and \
                    self.hash_table[ind][1] == hash_key:
                return ind
            ind = (ind + 1) % self.capacity

    def resize(self):
        if len(self) >= self.limit_to_resize:
            cash_hash_table = self.hash_table.copy()
            self.hash_table = [None] * len(cash_hash_table) * 2
            self.capacity = len(self.hash_table)
            self.limit_to_resize = self.capacity * 2 / 3
            for item in cash_hash_table:
                if item is not None:
                    (key, hash_key, value) = item
                    ind = hash_key % self.capacity
                    if self.hash_table[ind] is None:
                        self.hash_table[ind] = (key, hash_key, value)
                        continue
                    new_index = self.get_need_index(ind, key, hash_key)
                    self.hash_table[new_index] = (key, hash_key, value)

    def __setitem__(self, key, value):
        hash_key = hash(key)
        try:
            ind = hash_key % self.capacity
        except TypeError:
            return
        new_index = self.get_need_index(ind, key, hash_key)
        if self.hash_table[new_index] is None:
            self.__size += 1
        self.hash_table[new_index] = (key, hash_key, value)

        self.resize()

    def __getitem__(self, item):
        hash_key = hash(item)
        ind = hash_key % self.capacity
        if self.hash_table[ind] is None:
            raise KeyError
        while self.hash_table[ind]:
            if self.hash_table[ind][0] == item and \
                    self.hash_table[ind][1] == hash_key:
                return self.hash_table[ind][2]
            ind = (ind + 1) % self.capacity
        raise KeyError(item)

    def __len__(self):
        return self.__size

    def clear(self):
        self.hash_table = [None] * 8

    def __delitem__(self, item):
        hash_key = hash(item)
        need_item = [
            tup for tup in self.hash_table
            if tup is not None and tup[1] == hash_key and tup[0] == item]
        if len(need_item) > 0:
            self.hash_table[self.hash_table.index(need_item[0])] = None
            self.__size -= 1
        else:
            raise KeyError

    def get(self, item):
        return self.__getitem__(item)

    def update(self):
        self.resize()
