from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.capacity_table = 8
        self.size_dict = 0
        self.table = [None, None, None] * self.capacity_table

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if not isinstance(key, Hashable):
            raise TypeError("Key not hashable")
        key_hash = hash(key)
        index_table_cell = key_hash % self.capacity_table
        if self.table[index_table_cell] is None:
            self.table[index_table_cell] = [key, value, key_hash]
        else:

            while self.table[index_table_cell]:
                if (
                        self.table[index_table_cell][0] == key
                        and self.table[index_table_cell][2] == key_hash
                ):
                    self.table[index_table_cell][1] = value
                    return
                if self.table[
                    (index_table_cell + 1) % self.capacity_table
                ] is None:
                    self.table[
                        (index_table_cell + 1) % self.capacity_table
                    ] = [key, value, key_hash]
                    break
                index_table_cell = (index_table_cell + 1) % self.capacity_table
        self.size_dict += 1
        if self.size_dict > self.capacity_table * (2 / 3):
            self.resize_dict(self.table)

    def resize_dict(self, table_for_resize: list) -> None:
        self.capacity_table *= 2
        self.size_dict = 0
        self.table = [None] * self.capacity_table
        for item in table_for_resize:
            if item:
                self.__setitem__(item[0], item[1])

    def __getitem__(self, key: Hashable) -> Any:
        key_hash = hash(key)
        index_table_cell = key_hash % self.capacity_table
        while self.table[index_table_cell]:
            if self.table[index_table_cell][0] == key:
                return self.table[index_table_cell][1]
            index_table_cell = (index_table_cell + 1) % self.capacity_table
        raise KeyError(key)

    def __len__(self) -> int:
        return self.size_dict
