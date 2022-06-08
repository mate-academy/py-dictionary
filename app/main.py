class Dictionary:

    _DEFAULT_CAPACITY = 8
    _PERMITTED_VOLUME = 2 / 3

    def __init__(self):
        self._capacity = self._DEFAULT_CAPACITY
        self._size = 0
        self._array = [None] * self._capacity

    def __setitem__(self, key, value):
        index = self._index(key)

        while self._array[index] is not None:
            current_key = self._array[index][0]
            if key == current_key:
                self._array[index] = (current_key, value)
                return
            index += 1

        self._array[index] = (key, value)
        self._size += 1

        if self._size >= self._capacity * self._PERMITTED_VOLUME:
            self._resize()

    def __getitem__(self, search_key):
        index = self._index(search_key)

        while self._array[index] is not None:
            key, value = self._array[index]
            if key == search_key:
                return value
            index += 1

        raise KeyError

    def __len__(self):
        return self._size

    def _resize(self):
        included_elements = [
            element
            for element in self._array
            if element
        ]
        self._capacity *= 2
        self._size = 0
        self._array = [None] * self._capacity

        for key, value in included_elements:
            self.__setitem__(key=key, value=value)

    def _index(self, key):
        return hash(key) % self._capacity

    def __repr__(self):
        return "{" + ", ".join(
            f"{str(element[0])}: {str(element[1])}"
            for element in self._array
            if element is not None
        ) + "}"

    def clear(self):
        self._capacity = self._DEFAULT_CAPACITY
        self._size = 0
        self._array = [None] * self._capacity

    def __delitem__(self, del_key):
        self.pop(del_key)
        return

    def pop(self, pop_key):
        index = self._index(pop_key)

        while self._array[index] is not None:
            key, value = self._array[index]
            if key == pop_key:
                self._array[index] = None
                return value
            index += 1

        raise KeyError

    def __iter__(self):
        self.current_position = 0
        self._non_empty_arr = [
            element for element
            in self._array
            if element is not None
        ]
        print(self._non_empty_arr)
        return self

    def __next__(self):
        if self.current_position >= len(self._non_empty_arr):
            raise StopIteration

        return_value = self._non_empty_arr[self.current_position]
        self.current_position += 1

        return return_value

    def update(self, other):
        if not isinstance(other, Dictionary):
            raise ValueError

        for element in other._array:
            if element is not None:
                key, value = element
                self.__setitem__(key, value)
