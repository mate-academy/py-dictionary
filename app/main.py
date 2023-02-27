class Dictionary:
    threshold = 2 / 3

    def __init__(self):
        self._size = 8
        self._elements_num = 0
        self._hash_table = [[] for _ in range(self._size)]

    def __setitem__(self, key, value):
        hash_f = hash(key)
        index = hash_f % self._size

        while True:
            if not self._hash_table[index]:
                self._hash_table[index] = [key, hash_f, value]
                self._elements_num += 1

                break
            elif self._hash_table[index][0] == key:
                self._hash_table[index][2] = value

                break
            index = (index + 1) % self._size

        if self._elements_num == int(self._size * self.threshold):
            self.resize()

    def resize(self):
        temp_data = self._hash_table

        self._size *= 2
        self._elements_num = 0
        self._hash_table = [[] for _ in range(self._size)]

        for item in temp_data:
            if item:
                self.__setitem__(item[0], item[2])

    def __getitem__(self, key):
        hash_f = hash(key)
        index = hash_f % self._size

        while self._hash_table[index]:
            if self._hash_table[index][0] == key:
                return self._hash_table[index][2]
            index = (index + 1) % self._size

        raise KeyError(f"No key {key} in dictionary")

    def __len__(self):
        return self._elements_num
