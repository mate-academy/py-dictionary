from copy import deepcopy


class Dictionary:
    def __init__(self):
        self.capacity = 8
        self.threshold = int(self.capacity * 2 / 3)
        self.table = [[] for _ in range(self.capacity)]
        self.length = 0

    def __getitem__(self, key):
        hash_key = hash(key)
        get_index = hash_key % self.capacity

        while True:
            if not self.table[get_index]:
                raise KeyError

            try:
                if self.table[get_index][0] == key and \
                        self.table[get_index][2] == hash_key:
                    return self.table[get_index][1]
            except IndexError:
                raise KeyError
            get_index = (get_index + 1) % self.capacity

    def __setitem__(self, key, value):
        if self.length == self.threshold:
            self.upgrade_table()

        hash_key = hash(key)
        index = hash_key % self.capacity

        while True:
            if not self.table[index]:
                self.table[index] = [key, value, hash_key]
                self.length += 1
                break

            if hash_key == self.table[index][2] and \
                    key == self.table[index][0]:
                self.table[index][1] = value
                break

            index = (index + 1) % self.capacity

    def upgrade_table(self):
        copy_table = deepcopy(self.table)
        self.length = 0
        self.capacity *= 2
        self.threshold = int(self.capacity * 2 / 3)
        self.table = [[] for _ in range(self.capacity)]
        for element in copy_table:
            if element:
                self.__setitem__(element[0], element[1])

    def __len__(self):
        return self.length

    def get(self, key):
        return self.__getitem__(key)

    def clear(self):
        self.capacity = 8
        self.threshold = int(self.capacity * 2 / 3)
        self.length = 0
        self.table = [[] for _ in range(self.capacity)]
