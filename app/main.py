class Dictionary:

    def __init__(self):
        self.__capacity = 8
        self.__threshold = 2 / 3
        self.__resize_step = 3
        self.__cells = 0
        self.__hash_table = [None] * self.__capacity

    def __setitem__(self, key, value):
        if self.__cells > self.__capacity * self.__threshold:
            self.__hash_table_resize()
        cell_hash = hash(key)
        index = cell_hash % self.__capacity

        while self.__hash_table[index] is not None:
            if self.__hash_table[index][2] == cell_hash:
                if self.__hash_table[index][0] == key:
                    break
            index = (index + 1) % self.__capacity
        else:
            self.__cells += 1

        self.__hash_table[index] = (key, value, cell_hash)

    def __getitem__(self, key):
        cell_hash = hash(key)
        index = cell_hash % self.__capacity
        while self.__hash_table[index] is not None:
            if self.__hash_table[index][2] == cell_hash:
                if self.__hash_table[index][0] == key:
                    return self.__hash_table[index][1]
            index = (index + 1) % self.__capacity
        raise KeyError(f"Key: {key} not found.")

    def __len__(self):
        return self.__cells

    def clear(self):
        self.__cells = 0
        self.__hash_table = [None] * self.__capacity

    def __delitem__(self, key):
        if self[key]:
            index = hash(key) % self.__capacity
            self.__hash_table[index] = None
            self.__cells -= 1
        else:
            raise KeyError(f"Key: {key} not found.")

    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def pop(self, key, default=None):
        try:
            value = self.__getitem__(key)
            self.__delitem__(key)
        except KeyError:
            if default is not None:
                return default
            else:
                raise KeyError(f"Key: {key} not found.")
        return value

    def __hash_table_resize(self):
        hash_table = self.__hash_table
        self.__capacity *= self.__resize_step
        self.__hash_table = [None for _ in range(self.__capacity)]
        self.__cells = 0
        for cell in hash_table:
            if cell is not None:
                self.__setitem__(cell[0], cell[1])
