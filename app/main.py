from typing import Hashable, Any


class Dictionary:
    def __init__(self) -> None:
        self.hash_list = [None] * 8
        self.bucket_size = 8
        self.load_factor = 2 / 3
        self.threshold = int(self.bucket_size * self.load_factor)
        self.length = 0

    def find_item_index(self, item: Hashable) -> int:
        _hash = hash(item)
        index = _hash % len(self.hash_list)
        while self.hash_list[index] is not None:
            if self.hash_list[index][0] == item:
                return index
            index = (index + 1) % self.bucket_size

    def hash_expand(self) -> None:
        """Method expands and restructures hash table if its required"""

        hash_copy = self.hash_list.copy()
        self.bucket_size *= 2
        self.threshold = int(self.bucket_size * self.load_factor)
        self.hash_list = [None] * self.bucket_size
        self.length = 0
        for item in hash_copy:
            if item is not None:
                self.__setitem__(item[0], item[2])

    def __setitem__(self, key: Hashable, value: Any) -> Any:
        if self.length >= self.threshold:
            self.hash_expand()

        _hash = hash(key)
        index = _hash % len(self.hash_list)

        while True:
            if self.hash_list[index] is None:
                self.hash_list[index] = (key, _hash, value)
                self.length += 1
                break
            elif self.hash_list[index][0] == key:
                self.hash_list[index] = (key, _hash, value)
                break
            index = (index + 1) % self.bucket_size

    def __getitem__(self, item: Hashable) -> Any:
        index = self.find_item_index(item)
        if index is not None:
            return self.hash_list[index][2]
        raise KeyError(f"{item} is not in the dict")

    def __len__(self) -> int:
        return self.length

    def clear(self) -> None:
        self.hash_list = [None] * 8

    def __delitem__(self, key: Hashable) -> None:
        index = self.find_item_index(key)
        if index is not None:
            self.hash_list[index] = None
        raise KeyError(f"{key} is not in the dict")

    def get(self, key: Hashable, value: Any = None) -> Any:
        index = self.find_item_index(key)
        if index is not None:
            return self.hash_list[index][2]
        return value

    def pop(self, key: Hashable) -> Any:
        index = self.find_item_index(key)
        if index is not None:
            value = self.hash_list[index]
            self.hash_list[index] = None
            return value
        raise KeyError(f"{key} is not in the dict")

    def update(self, **kwargs) -> None:
        if kwargs is not None:
            for item, value in kwargs.items():
                self.__setitem__(item, value)

    def __iter__(self) -> Any:
        self.iter_list = []
        for item in self.hash_list:
            if item is not None:
                self.iter_list.append(item)
        self.index = 0
        return self

    def __next__(self) -> Any:
        if self.index < self.__len__():
            result = self.iter_list[self.index]
            self.index += 1
            return result[0]
        else:
            raise StopIteration

    def __repr__(self) -> str:
        return f"{self.hash_list}"

    def __str__(self) -> str:
        self.str_list = []
        for item in self.hash_list:
            if item is not None:
                self.str_list.append(f"{item[0]}: {item[2]}")
        return f"{self.str_list}"
