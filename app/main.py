class Dictionary:
    def __init__(self):
        self.length = 0
        self.capacity = 8
        self.load_factor = 2 / 3
        self.threshold = self.capacity * self.load_factor
        self.hash_table = [[]for _ in range(self.capacity)]

    def __setitem__(self, key, value):
        if self.length > self.threshold:
            self.rebuilding_hash_table()
        self.add_new_element(key, value)

    def __getitem__(self, item):
        hashed_value = hash(item)
        index = hashed_value % self.capacity
        while self.hash_table[index]:
            if self.hash_table[index][1] == item \
                    and self.hash_table[index][0] == hashed_value:
                return self.hash_table[index][2]
            index = (index + 1) % self.capacity
        raise KeyError

    def rebuilding_hash_table(self):
        self.capacity *= 2
        self.length = 0
        self.threshold = self.capacity * self.load_factor
        prev_list = [item for item in self.hash_table if item]
        self.hash_table = [[] for _ in range(self.capacity)]
        for item in prev_list:
            self.__setitem__(item[1], item[2])

    def add_new_element(self, key, value):
        hashed_value = hash(key)
        index = hashed_value % self.capacity
        while True:
            if len(self.hash_table[index]) == 0:
                self.hash_table[index] = [hashed_value, key, value]
                self.length += 1
                break

            if key == self.hash_table[index][1] \
                    and self.hash_table[index][0] == hashed_value:
                self.hash_table[index] = [hashed_value, key, value]
                break
            index = (index + 1) % self.capacity

    def __len__(self):
        return self.length
