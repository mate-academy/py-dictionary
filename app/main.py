from typing import Hashable

import copy


class DictionaryMember:
    def __init__(
            self,
            key: Hashable,
            value: any,
            index: int = None
    ) -> None:
        self.key = key
        self.value = value
        self.index = index


class Dictionary:

    def __init__(
            self,
            capacity: int = 10,
            load_factor: float = 0.7
    ) -> None:

        self.size = 0
        self.capacity = capacity
        self.load_factor = load_factor
        self.table = [None] * self.capacity

    def _index(
            self,
            key: Hashable
    ) -> int:

        index = hash(key) % self.capacity

        if (
                self.table[index] is None
                or (self.table[index].key == key
                    and hash(self.table[index].key) == hash(key))
        ):
            return index

        else:
            while (
                    self.table[index] is not None
                    and self.table[index].key != key
            ):
                index += 1
                if index > (len(self.table) - 1):
                    index = 0
            return index

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        old_table = copy.deepcopy(self.table)
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0

        for member in old_table:
            try:
                self.__setitem__(
                    key=member.key,
                    value=member.value)
            except AttributeError:
                pass

    def __setitem__(
            self,
            key: int | str | tuple | float,
            value: any
    ) -> None:

        key_index = self._index(key)

        if self.table[key_index] is None:
            self.table[key_index] = DictionaryMember(key=key,
                                                     value=value)
            self.size += 1
            print("Data has added successfully!")
        else:
            self.table[key_index].value = value
            print("Data has written successfully!")

        if self.size / self.capacity > self.load_factor:
            self._resize()

    def __getitem__(
            self,
            key: int | str | tuple | float
    ) -> any:

        index = self._index(key)
        current = self.table[index]

        if current is None:
            raise KeyError

        else:
            return current.value

    def _clear(self) -> None:
        self.table = [None] * self.capacity
        print("All data in this dictionary was removed!")

    def __delitem__(
            self,
            key: int | str | tuple | float
    ) -> None:

        try:
            element = self.__getitem__(key)
        except AttributeError:
            print("This key is not exist in this dictionary!")
        else:
            element_index = self.table.index(element)
            self.table[element_index] = None
            print(f"Item with key {key} was removed!")
