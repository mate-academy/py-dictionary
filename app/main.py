class Dictionary:

    def __init__(self):
        self._capacity = 8
        self._threshold = self._capacity * 2 / 3
        self._size = 0
        self._hash_table = [None for _ in range(self._capacity)]

    def __getitem__(self, key):
        hash_key = hash(key)
        index_ = hash_key % self._capacity

        while self._hash_table[index_]:
            if self._hash_table[index_][0] == hash_key \
                    and self._hash_table[index_][1] == key:
                return self._hash_table[index_][2]
            index_ = (index_ + 1) % self._capacity

        raise KeyError(f"Key {key} not found in dictionary")

    def __setitem__(self, key, value):
        if self._size >= self._threshold:
            self._resize()

        hash_key = hash(key)
        index_ = hash_key % self._capacity

        while True:
            if not self._hash_table[index_]:
                self._hash_table[index_] = [hash_key, key, value]
                self._size += 1
            if self._hash_table[index_][0] == hash_key \
                    and self._hash_table[index_][1] == key:
                self._hash_table[index_][2] = value
                break
            index_ = (index_ + 1) % self._capacity

    def __delitem__(self, key):
        hash_key = hash(key)
        index_ = hash_key % self._capacity

        while self._hash_table[index_]:
            if self._hash_table[index_][0] == hash_key and \
                    self._hash_table[index_][1] == key:
                value = self._hash_table[index_][2]
                self._hash_table[index_] = None
                self._size -= 1
                return value
            index_ = (index_ + 1) % self._capacity

        raise KeyError(f"Key {key} not found in dictionary")

    def __len__(self):
        return self._size

    def __iter__(self):
        self._it = 0
        self._array = [element for element in self._hash_table
                       if element is not None]
        return self

    def __next__(self):
        if self._it >= len(self._array):
            raise StopIteration

        node = self._array[self._it]
        self._it += 1
        return node

    def get(self, key, value=None):
        try:
            return self.__getitem__(key)
        except KeyError:
            return value

    def _resize(self):
        old_data = [elements for elements in self._hash_table if elements]
        self._capacity *= 2
        self._size = 0
        self._threshold = self._capacity * 2 / 3
        self._hash_table = [None] * self._capacity

        for elements in old_data:
            if elements:
                self.__setitem__(key=elements[1], value=elements[2])

    def pop(self, key):
        try:
            value = self[key]
            self.__delitem__(key)
            return value
        except KeyError:
            raise f"Key {key} not found in dictionary"

    def update(self, *args, **kwargs):
        for arg in args:
            if isinstance(arg, dict):
                for key, value in arg.items():
                    self.__setitem__(key, value)
            else:
                key, value = arg
                self.__setitem__(key, value)

        for key, value in kwargs.items():
            self.__setitem__(key, value)

    def clear(self):
        self._hash_table = [None for _ in self._hash_table]
        self._size = 0
