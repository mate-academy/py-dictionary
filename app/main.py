class Dictionary:
    def __init__(self):
        self._capacity = 8
        self._border = 2 / 3
        self._size = 0
        self._increase = 2
        self._hash_table = [None for _ in range(self._capacity)]

    def __getitem__(self, key):
        hash_ = hash(key)
        index = hash_ % self._capacity
        while self._hash_table[index]:
            if self._hash_table[index][0] == hash_ and (
                    self._hash_table[index][1] == key):
                return self._hash_table[index][2]
            index = (index + 1) % self._capacity
        else:
            raise KeyError(f"Key: {key} not in dictionary!")

    def __setitem__(self, key, value):
        if self._size + 1 > self._capacity * self._border:
            self._doubling_hash_table()
        hash_ = hash(key)
        index = hash_ % self._capacity
        obj = [hash_, key, value]
        while self._hash_table[index] is not None:
            if self._hash_table[index][0] == hash_ and \
                    self._hash_table[index][1] == key:
                self._hash_table[index][2] = value
                return

            index = (index + 1) % self._capacity

        self._hash_table[index] = obj
        self._size += 1

    def _doubling_hash_table(self):
        elements = [
            el
            for el in self._hash_table
            if el is not None
        ]
        self._capacity *= self._increase
        self._hash_table = [None for _ in range(self._capacity)]
        self._size = 0
        for el in elements:
            self.__setitem__(el[1], el[2])

    def __len__(self):
        return self._size

    def __repr__(self):
        return repr(self.__dict__)
