class Dictionary:

    def __init__(self):
        self.capacity = 8
        self.length = 0
        self.t_hold = int(self.capacity * (2 / 3))
        self.hash_table = [[] for _ in range(self.capacity)]

    def adding_item(self, key, value):
        hash_code = hash(key)
        hash_index = hash_code % self.capacity
        while True:
            if not self.hash_table[hash_index]:
                self.hash_table[hash_index].extend([key, value, hash_code])
                self.length += 1
                break
            if self.hash_table[hash_index][2] == hash_code \
                    and self.hash_table[hash_index][0] == key:
                self.hash_table[hash_index][1] = value
                break
            hash_index = (hash_index + 1) % self.capacity

    def __setitem__(self, key, value):
        if self.length < self.t_hold:
            self.adding_item(key, value)
        else:
            temporary_storage = self.hash_table
            self.capacity *= 2
            self.length = 0
            self.hash_table = [[] for _ in range(self.capacity)]
            self.t_hold = int(self.capacity * (2 / 3))
            for item in temporary_storage:
                if item:
                    self.adding_item(item[0], item[1])
            self.adding_item(key, value)

    def __getitem__(self, key):
        hash_code = hash(key)
        hash_index = hash_code % self.capacity
        while self.hash_table[hash_index]:
            if self.hash_table[hash_index][2] == hash_code \
                    and self.hash_table[hash_index][0] == key:
                return self.hash_table[hash_index][1]
            hash_index = (hash_index + 1) % self.capacity
        raise KeyError

    def __len__(self):
        return self.length
