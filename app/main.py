class Dictionary:
    def __init__(self):
        self.capacity = 8
        self.hash_table = [[] for _ in range(self.capacity)]
        self.size = 0

    def __setitem__(self, key, value):
        threshold = int((self.capacity * 2 / 3))

        if self.size == threshold:
            self.resize()

        hash_ = hash(key) % self.capacity
        self.hashing(hash_, value, key)

    def resize(self):
        self.capacity *= 2
        self.size = 0
        old_hash_table = self.hash_table
        self.hash_table = [[] for _ in range(self.capacity)]
        for element in old_hash_table:
            if len(element) != 0:
                self.hashing(hash(element[0]) % self.capacity,
                             element[1],
                             element[0])

    def __getitem__(self, key):
        index_item = hash(key) % self.capacity
        if len(self.hash_table[index_item]) == 0:
            raise KeyError

        while self.hash_table[index_item][0] != key:
            index_item = (index_item + 1) % self.capacity
            if index_item >= len(self.hash_table):
                raise KeyError

        if self.hash_table[index_item][0] == key \
                and hash(self.hash_table[index_item][0]) == hash(key):
            return self.hash_table[index_item][1]

    def __len__(self):
        return self.size

    def hashing(self, hash_, value, key_):
        while True:
            if len(self.hash_table[hash_]) == 0:
                self.hash_table[hash_] = [key_, value, hash_]
                self.size += 1
                break
            elif self.hash_table[hash_][0] == key_:
                self.hash_table[hash_] = [key_, value, hash_]
                break
            if hash_ == self.capacity - 1:
                for res_index in range(self.capacity):
                    if not self.hash_table[res_index]:
                        self.hash_table[res_index] = [key_, value, hash_]
                        self.size += 1
                        break
            hash_ += 1
            if hash_ >= len(self.hash_table):
                break
