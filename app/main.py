import copy
from typing import Union, Any


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.hash_table = [[] for _ in range(self.capacity)]

    def __setitem__(self,
                    key: Union[int, float, str, tuple, bool],
                    value: Any
                    ) -> None:

        if self.length >= self.capacity * 2 / 3:
            self.resize()

        self.adding_item(key, value)

    def resize(self) -> None:
        self.length = 0
        self.capacity *= 2
        old_table = copy.deepcopy(self.hash_table)
        self.hash_table = [[] for _ in range(self.capacity)]
        for item in old_table:
            if len(item) > 1:
                self.adding_item(item[0], item[2])

    def adding_item(self,
                    key: Union[int, float, str, tuple, bool],
                    value: Any
                    ) -> None:
        hash_key = hash(key)
        index_value = hash_key % self.capacity
        while True:
            if not self.hash_table[index_value]:
                self.hash_table[index_value] = ([key, hash_key, value])
                self.length += 1
                break
            if self.hash_table[index_value][1] == hash_key \
                    and self.hash_table[index_value][0] == key:
                self.hash_table[index_value][2] = value
                break
            index_value = (index_value + 1) % len(self.hash_table)

    def __getitem__(self,
                    key: Union[int, float, str, tuple, bool]
                    ) -> Any:
        hash_key = hash(key)
        index_value = hash_key % self.capacity

        while True:
            if not self.hash_table[index_value]:
                raise KeyError(key)
            if self.hash_table[index_value][1] == hash_key \
                    and self.hash_table[index_value][0] == key:
                return self.hash_table[index_value][2]
            index_value = (index_value + 1) % len(self.hash_table)

    def __len__(self) -> int:
        return self.length
