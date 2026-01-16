class Dictionary:
    _CAPACITY_FACTOR = 8
    _LOAD_FACTOR = 2 / 3

    def __init__(self):
        self._capacity = self._CAPACITY_FACTOR
        self._size = 0
        self._table = [None] * self._capacity

    def __setitem__(self, key, value):
        index = self._index(hash(key))
        while self._table[index] is not None:
            current_key, _ = self._table[index]
            if key == current_key:
                self._table[index] = (current_key, value)
                return
            index = self._index(index + 1)

        self._table[index] = (key, value)
        self._size += 1

        if self._size >= self._capacity * self._LOAD_FACTOR:
            self._resize()

    def __getitem__(self, item):
        index = self._index(hash(item))
        while self._table[index] is not None:
            key, value = self._table[index]
            if key == item:
                return value
            index = self._index(index + 1)
        raise KeyError

    def _resize(self):
        old = [item for item in self._table if item]
        self._capacity *= 2
        self._size = 0
        self._table = [None] * self._capacity

        for key, value in old:
            self[key] = value

    def __len__(self):
        return self._size

    def _index(self, hashed_value):
        return hashed_value % self._capacity
