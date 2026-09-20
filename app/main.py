from typing import Any


class Dictionary:
    def __init__(self, key: Any = None, value: Any = None) -> None:
        self.slots = 8
        self.key = key
        self.value = value
        self.hash_table = [None] * self.slots

    def __setitem__(self, key: Any, value: Any) -> None:
        capacity = self.__len__()
        if capacity >= (0.67 * len(self.hash_table)):
            self.slots *= 2
            old_table = self.hash_table
            self.hash_table = [None] * self.slots
            for elem in old_table:
                if elem is not None:
                    self[elem[0]] = elem[2]
        if self.hash_table[self.get_hash(key)] is None:
            self.hash_table[self.get_hash(key)] =\
                (key, self.get_hash(key), value)
        elif key == self.hash_table[self.get_hash(key)][0]:
            self.hash_table[self.get_hash(key)] = \
                (key, self.get_hash(key), value)
        else:
            ind = (self.get_hash(key) + 1) % len(self.hash_table)
            while (self.hash_table[ind] is not None
                   and self.hash_table[ind][0] != key):
                ind += 1
                ind %= len(self.hash_table)
            self.hash_table[ind] = (key, ind, value)

    def __getitem__(self, key: Any) -> Any:
        if self.hash_table[self.get_hash(key)] is None:
            raise KeyError
        elif key == self.hash_table[self.get_hash(key)][0]:
            return self.hash_table[self.get_hash(key)][2]
        else:
            ind = (self.get_hash(key) + 1) % len(self.hash_table)
            while (self.hash_table[ind] is not None
                   and self.hash_table[ind][0] != key):
                ind += 1
                ind %= len(self.hash_table)
            if self.hash_table[ind] is None:
                raise KeyError
            return self.hash_table[ind][2]

    def __len__(self) -> int:
        lght = 0
        for elem in self.hash_table:
            if elem is not None:
                lght += 1
        return lght

    def get_hash(self, key: Any) -> int:
        return hash(key) % len(self.hash_table)
