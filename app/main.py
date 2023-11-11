class Dictionary:
    _DEFAULT_LENGTH = 8
    _LOAD_COEFFICIENT = 0.6666666666666667  # 2 / 3

    def __init__(self):
        self._length = self._DEFAULT_LENGTH
        self._size = 0
        self._hash_table = [None] * self._length

    def __setitem__(self, key, value):
        index = self._index(hash(key))
        while self._hash_table[index] is not None:
            current_key, _ = self._hash_table[index]
            if key == current_key:
                self._hash_table[index] = (current_key, value)
                return
            index = self._index(index + 1)

        self._hash_table[index] = (key, value)
        print(self._hash_table)
        self._size += 1

        if self._size >= self._length * self._LOAD_COEFFICIENT:
            self._resize()

    def __getitem__(self, item):
        index = self._index(hash(item))
        while self._hash_table[index] is not None:
            key, value = self._hash_table[index]
            if key == item:
                return value
            index = self._index(index + 1)
        raise KeyError

    def _resize(self):
        _past_value = [item for item in self._hash_table if item]
        self._length *= 2
        self._size = 0
        self._hash_table = [None] * self._length

        for key, value in _past_value:
            self.__setitem__(key, value)

    def __len__(self):
        return self._size

    def _index(self, hashed_value):
        return hashed_value % self._length
