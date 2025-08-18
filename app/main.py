from collections.abc import Hashable, Iterable
from typing import Any


class Dictionary:

    def __init__(self, elements: None) -> None:
        if not elements:
            elements = []
        if not isinstance(elements, Iterable):
            raise TypeError(f"Non-iterable type: '{type(elements)}'")
        else:
            self.__load_factor = 0.66  # 2/3
            self.__table_size = 2 ** (
                (len(elements).bit_length()
                 if len(elements).bit_length() > 2 else 2) + 1)
            self.__buckets = [None, ] * self.__table_size
            self.__occupied = 0
            self.__assign_elements(elements)

    def __table_resizing(self, new_size: int | float) -> None:
        temp_buckets = [bucket for bucket in self.__buckets if bucket]
        self.__occupied = len(temp_buckets)
        self.__table_size = int(self.__table_size * new_size)
        self.__buckets = [None, ] * self.__table_size
        self.__occupied = 0
        self.__assign_elements(temp_buckets)

    def __assign_elements(self, elements: tuple) -> None:
        for element in elements:
            if element and len(element) != 2:
                raise ValueError(
                    "Can't insert the element",
                    element,
                    "due to it's incorrect format."
                )
            else:
                self.__setitem__(element[0], element[1])

        if self.__occupied >= (self.__table_size * self.__load_factor):
            self.__table_resizing(2)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if not isinstance(key, Hashable):
            raise TypeError(f"Unhashable key {key}")
        hashed_value = hash(key)
        index = hashed_value % self.__table_size
        done = False
        for index in range(index, self.__table_size):
            if self.__buckets[index] is None:
                self.__buckets[index] = (key, value)
                self.__occupied += 1
                done = True
                break
            elif self.__buckets[index][0] == key:
                self.__buckets[index] = (key, value)
                done = True
                break
        if not done:
            self.__table_resizing(2)
            return self.__setitem__(key, value)

    def __getitem__(self, key: Hashable) -> Any:
        if not isinstance(key, Hashable):
            raise TypeError(f"Unhashable key {key}")
        hashed_value = hash(key)
        index = hashed_value % self.__table_size
        done = False
        for index in range(index, self.__table_size):
            if self.__buckets[index] and self.__buckets[index][0] == key:
                done = True
                return self.__buckets[index][1]
        if not done:
            raise KeyError("No such key", key)

    def __len__(self) -> int:
        return self.__occupied

    def __repr__(self) -> str:
        res = "{"
        for pair in self.__buckets:
            if pair:
                res += f"({pair[0]} : {pair[1]}), "
        return res[:-2] + "}"

    def __delitem__(self, key: Hashable) -> None:
        if not isinstance(key, Hashable):
            raise TypeError(f"Unhashable key {key}")
        hashed_value = hash(key)
        index = hashed_value % self.__table_size
        found = False
        while index <= self.__table_size:
            if self.__buckets[index] and self.__buckets[index][0] == key:
                self.__buckets[index] = None
                self.__occupied -= 1
                found = True
                break
            else:
                index += 1
        if not found:
            raise KeyError("No such key", key)
        if self.__occupied < (self.__table_size / 2):
            self.__table_resizing(0.5)

    def keys(self) -> list:
        res = []
        for pair in self.__buckets:
            if pair:
                res.append(pair[0])
        return res


if __name__ == "__main__":
    pass
