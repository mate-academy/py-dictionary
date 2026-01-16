class Dictionary:
    def __init__(self):
        self.capacity = 8
        self.size = 0
        self.threshold = int(self.capacity * 2 / 3)
        self.hash_table = [[] for _ in range(self.capacity)]

    def __setitem__(self, key, value):
        if self.size == self.threshold:
            self.change_size()
        hash_code = hash(key)
        self.add_to_hash_table(key, value, hash_code)

    def change_size(self):
        self.size = 0
        self.capacity *= 2
        self.threshold = int(self.capacity * 2 / 3) + 1
        old_hash_table = self.hash_table
        self.hash_table = [[] for _ in range(self.capacity)]
        for item in old_hash_table:
            if item != []:
                self.__setitem__(item[0], item[1])

    def add_to_hash_table(self, key, value, hash_code):
        index_item = hash_code % self.capacity

        while True:
            if self.hash_table[index_item] == []:
                self.size += 1
                self.hash_table[index_item] = [key, value, hash_code]
                break
            if self.hash_table[index_item][2] == hash_code \
                    and self.hash_table[index_item][0] == key:
                self.hash_table[index_item][1] = value
                break
            index_item = (index_item + 1) % self.capacity

    def __getitem__(self, key):
        hash_code = hash(key)
        index_item = hash_code % self.capacity

        while self.hash_table[index_item] != []:
            if self.hash_table[index_item][2] == hash_code \
                    and self.hash_table[index_item][0] == key:
                return self.hash_table[index_item][1]
            index_item = (index_item + 1) % self.capacity
        raise KeyError

    def __len__(self):
        return self.size
