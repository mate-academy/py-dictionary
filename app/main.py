import math
from typing import Hashable, Any


class Dictionary:
    def __init__(self) -> None:
        self.len_elem = 0
        self.capacity = 8
        self.kf_load = 2 / 3
        self.hash_table: list = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.len_elem == math.floor(self.capacity * self.kf_load):
            temp = self.hash_table.copy()
            self.len_elem = 0
            self.capacity = self.capacity * 2
            self.hash_table = [None] * self.capacity
            for old_hash_el in temp:
                if old_hash_el is None or old_hash_el == "del_elm":
                    continue
                self.find_free_space(old_hash_el[0], old_hash_el[2])
            self.find_free_space(key, value)
        else:
            self.find_free_space(key, value)

    def __getitem__(self, key: Hashable) -> Any:
        first_index = hash(key) % self.capacity
        if (self.hash_table[first_index] is None
                or self.hash_table[first_index] == "del_elm"):
            pass
        else:
            if self.hash_table[first_index][0] == key:
                return self.hash_table[first_index][2]
        index = (list(range(first_index, self.capacity))
                 + list(range(0 , first_index)))
        for i in index:
            if self.hash_table[i] is None:
                continue
            if self.hash_table[i][0] == key:
                return self.hash_table[i][2]
        raise KeyError("Key not found")

    def __len__(self) -> int:
        return self.len_elem

    def __delitem__(self, key: Hashable) -> None:
        first_index = hash(key) % self.capacity
        if self.hash_table[first_index] is None:
            pass
        else:
            if self.hash_table[first_index][0] == key:
                self.hash_table[first_index] = "del_elm"
                self.len_elem -= 1
                return None
        index = (list(range(first_index, self.capacity))
                 + list(range(0, first_index)))
        for i in index:
            if self.hash_table[i] is None:
                continue
            if self.hash_table[i][0] == key:
                self.hash_table[i] = "del_elm"
                self.len_elem -= 1
                return None
        raise KeyError("Key not found")

    def find_free_space(self, key: Hashable, value: Any) -> None:
        index = hash(key) % self.capacity
        while True:
            if (self.hash_table[index] is None
                    or self.hash_table[index] == "del_elm"):
                self.hash_table[index] = (key, hash(key), value)
                self.len_elem += 1
                break
            else:
                if key == self.hash_table[index][0]:
                    self.hash_table[index] = (key, hash(key), value)
                    break
                if index == self.capacity - 1:
                    index = 0
                else:
                    index += 1

    def clear(self) -> None:
        self.len_elem = 0
        self.capacity = 8
        self.hash_table: list = [None] * self.capacity
