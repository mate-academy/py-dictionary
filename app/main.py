class Dictionary:
    def __init__(self):
        self.length = 0
        self.capacity = 8
        self.hash_table = [[] for _ in range(self.capacity)]

    def __len__(self):
        return self.length

    def __setitem__(self, key, value):
        if len(self) + 1 > self.capacity * 2 / 3:
            self._resize()
        hash_ = hash(key)
        index = hash_ % self.capacity
        while True:
            if len(self.hash_table[index]) > 0:
                if hash_ == self.hash_table[index][0] \
                        and key == self.hash_table[index][1]:
                    self.hash_table[index] = [hash_, key, value]
                    break
                index = (index + 1) % self.capacity
            else:
                self.hash_table[index] = [hash_, key, value]
                self.length += 1
                break

    def __getitem__(self, key):
        hash_ = hash(key)
        index = hash_ % self.capacity
        i = 0
        while i <= self.capacity:
            if len(self.hash_table[index]) > 0:
                if self.hash_table[index][0] == hash_ \
                        and self.hash_table[index][1] == key:
                    return self.hash_table[index][2]
                index = (index + 1) % self.capacity
            i += 1
        raise KeyError

    def _resize(self):
        previous_list = []
        for item in self.hash_table:
            if len(item) > 0:
                previous_list.append(item)
        self.capacity *= 2
        self.hash_table = [[] for _ in range(self.capacity)]
        for item in previous_list:
            index = item[0] % self.capacity
            while True:
                if len(self.hash_table[index]) > 0:
                    index = (index + 1) % self.capacity
                else:
                    self.hash_table[index] = item
                    break
