class Dictionary:
    def __init__(self):
        self._capacity = 8
        self._length = 0
        self._hash_table = [[] for _ in range(self._capacity)]

    def __setitem__(self, key, value):
        self._length += 1
        self._check_load_factor()

        index = hash(key) % self._capacity

        while self._hash_table[index]:
            if self._hash_table[index][0] == key:
                self._length -= 1
                self._hash_table[index][2] = value
                return

            index = self._increase_index(index)

        self._hash_table[index] = [key, hash(key), value]

    def _check_load_factor(self):
        if len(self) > int(self._capacity * 2 / 3):
            self._resize()

    def _resize(self):
        self._capacity *= 2
        old_hash_table = self._hash_table
        self._hash_table = [[] for _ in range(self._capacity)]

        for item in old_hash_table:
            if item:
                new_index = item[1] % self._capacity

                while self._hash_table[new_index]:
                    new_index = self._increase_index(new_index)

                self._hash_table[new_index] = item

    def _increase_index(self, index):
        index += 1
        if index == self._capacity:
            index = 0
        return index

    def __getitem__(self, key):
        index = hash(key) % self._capacity

        while self._hash_table[index]:
            if self._hash_table[index][0] == key:
                return self._hash_table[index][2]

            index = self._increase_index(index)

        raise KeyError(key)

    def __len__(self):
        return self._length
