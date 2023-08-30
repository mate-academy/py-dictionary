from typing import Any


class Dictionary:
    _DEFAULT_CAPACITY = 8
    _GET_RESIZE = 2 / 3
    _GET_NEW_CAPACITY = 2

    def __init__(self):
        self._capacity = Dictionary._DEFAULT_CAPACITY
        self._data_list: Any = [None for _ in range(self._capacity)]
        self._len_data_list = 0

    @property
    def _threshold(self):
        return int(self._capacity * Dictionary._GET_RESIZE)

    def __setitem__(self, key, value):
        hash_ = hash(key)

        position: int = hash_ % self._capacity

        while self._data_list[position] is not None:
            current_data = self._data_list[position]
            if hash_ == current_data[2] and key == current_data[0]:
                current_data[1] = value
                return

            position = (position + 1) % self._capacity

        self._data_list[position] = [key, value, hash_]

        self._len_data_list += 1

        if self.__len__() == self._threshold:
            self._len_data_list = 0
            self._resize()

    def __len__(self):
        return self._len_data_list

    def _resize(self):
        self._capacity *= Dictionary._GET_NEW_CAPACITY
        list_data = [i for i in self._data_list if i is not None]
        self._data_list = [None for _ in range(self._capacity)]
        for data in list_data:
            self.__setitem__(data[0], data[1])

    def __getitem__(self, item):
        position = hash(item) % self._capacity

        while self._data_list[position] is not None:
            current_data = self._data_list[position]

            if item == current_data[0]:
                return current_data[1]

            position = (position + 1) % self._capacity

        raise KeyError
