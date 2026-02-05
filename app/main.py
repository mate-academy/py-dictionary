class Dictionary:
    def __init__(self):
        self.capacity = 8
        self.threshold = self.capacity * (2 / 3)
        self.size_now = 0
        self.hash_table = [None] * self.capacity

    def __setitem__(self, key, value):
        if self.size_now <= self.threshold:
            tmp_hash = hash(key)
            tmp_index = tmp_hash % self.capacity
            if not self.hash_table[tmp_index]:
                self.hash_table[tmp_index] = [key, tmp_hash, value]
                self.size_now += 1
            else:
                if self.hash_table[tmp_index][0] == key:
                    self.hash_table[tmp_index][2] = value
                else:
                    for i in range(tmp_index):
                        index = (tmp_index + i) % self.capacity
                        if not self.hash_table[index]:
                            self.hash_table[index] = [key, tmp_hash, value]
                            self.size_now += 1
                            break
        else:
            tmp_hash_table = self.hash_table.copy()
            self.capacity *= 2
            self.size_now = 0
            self.hash_table.clear()
            self.threshold = self.capacity * (2 / 3)
            self.hash_table = [None] * self.capacity
            for element in tmp_hash_table:
                if element:
                    self.__setitem__(element[0], element[2])
            self.__setitem__(key, value)

    def __getitem__(self, key):
        tmp_index = hash(key) % self.capacity
        if self.hash_table[tmp_index]:
            if self.hash_table[tmp_index][0] == key:
                return self.hash_table[tmp_index][2]
        else:
            for i in range(tmp_index):
                index = (tmp_index + i) % self.capacity
                if self.hash_table[index]:
                    if self.hash_table[index][0] == key:
                        return self.hash_table[index][2]
        raise KeyError(f"Key '{key}' not found")

    def __len__(self):
        return self.size_now
