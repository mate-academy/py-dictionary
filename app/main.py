class Dictionary:
    def __init__(self):
        self.capacity = 8
        self.hash_table = [None for _ in range(self.capacity)]
        self.size = 0

    def __getitem__(self, item):
        key_hash = hash(item)
        index = key_hash % self.capacity
        while self.hash_table[index]:
            if self.hash_table[index][0] == key_hash and \
                    self.hash_table[index][1] == item:
                return self.hash_table[index][2]
            index = (index + 1) % self.capacity
        raise KeyError(f"Key: {item} not in dictionary!")

    def __setitem__(self, key, value):
        self.resize()

        key_hash = hash(key)
        index = key_hash % self.capacity
        while self.hash_table[index]:
            if self.hash_table[index][0] == key_hash and \
                    self.hash_table[index][1] == key:
                self.hash_table[index][2] = value
                self.size -= 1
                break
            else:
                index = (index + 1) % self.capacity
        self.hash_table[index] = [key_hash, key, value]
        self.size += 1

    def __len__(self):
        return self.size

    def __repr__(self):
        return str(
            {key[0]: key[-1] for key in self.hash_table if key is not None}
        )

    def resize(self):
        if self.size > self.capacity * 2 / 3:
            self.capacity *= 2

            copy_hash_table = self.hash_table.copy()
            self.hash_table = [[] for _ in range(self.capacity)]
            self.size = 0
            for element in copy_hash_table:
                if element:
                    self.__setitem__(element[1], element[2])
