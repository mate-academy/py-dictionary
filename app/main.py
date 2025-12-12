from typing import Hashable, Any


class Dictionary:
    DELETED = object()

    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = 2 / 3
        self.threshold = 5
        self.size = 0
        self.hash_table: list = [[None] for _ in range(self.capacity)]

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size == self.threshold:
            self.table_hash_resize()

        key_hash = hash(key)
        hash_table_index = key_hash % self.capacity

        for _ in range(self.capacity):
            if hash_table_index == self.capacity:
                hash_table_index = 0
            if (
                not self.hash_table[hash_table_index][0]
                or self.hash_table[hash_table_index][0] is Dictionary.DELETED
            ):
                self.hash_table[hash_table_index] = [key, key_hash, value]
                self.size += 1
                break
            if self.hash_table[hash_table_index][0] == key:
                self.hash_table[hash_table_index][2] = value
                break
            hash_table_index += 1

    def __getitem__(self, key: Hashable) -> Any:
        key_hash = hash(key)
        hash_table_index = key_hash % self.capacity

        for _ in range(self.capacity):
            if hash_table_index == self.capacity:
                hash_table_index = 0
            if not self.hash_table[hash_table_index][0]:
                raise KeyError(key)
            if self.hash_table[hash_table_index][0] == key:
                return self.hash_table[hash_table_index][2]
            hash_table_index += 1

    def table_hash_resize(self) -> None:
        self.capacity *= 2
        self.threshold = int(self.capacity * self.load_factor)
        outdated_hash_table = self.hash_table
        self.clear()

        for item in outdated_hash_table:
            if item[0]:
                self.__setitem__(item[0], item[2])

        del outdated_hash_table

    def __len__(self) -> int:
        return self.size

    def clear(self) -> None:
        self.hash_table = [[None] for _ in range(self.capacity)]
        self.size = 0

    def __delitem__(self, key: Hashable) -> None:
        self.__getitem__(key)
        key_hash = hash(key)
        hash_table_index = key_hash % self.capacity

        for _ in range(self.capacity):
            if hash_table_index == self.capacity:
                hash_table_index = 0
            if self.hash_table[hash_table_index][0] == key:
                self.hash_table[hash_table_index][0] = Dictionary.DELETED
                break
            hash_table_index += 1

    def get(self, key: Hashable) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return None

    def pop(self, key: Hashable) -> Any:
        return_value = self.__getitem__(key)
        self.__delitem__(key)
        return return_value

    def update(self, dictionary: "Dictionary") -> None:
        for item in dictionary.hash_table:
            if not item[0] or item[0] is not Dictionary.DELETED:
                self.__setitem__(item[0], item[2])
