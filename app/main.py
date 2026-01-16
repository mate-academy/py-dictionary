from typing import Any, Generator


class Dictionary:

    def __init__(self) -> None:
        self.max_capacity = 8
        self.threshold = self.max_capacity - (self.max_capacity * 2 // 3)
        self.hash_table = [None] * self.max_capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.hash_table.count(None) <= self.threshold:
            self.resize_table()
        index = self.find_index(key)
        self.hash_table[index] = (key, value)

    def __getitem__(self, key: Any) -> Any:
        index = self.find_value_from_key(key)
        if self.hash_table[index]:
            return self.hash_table[index][1]
        else:
            raise KeyError("Key not found")

    def __len__(self) -> int:
        return len(self.hash_table) - self.hash_table.count(None)

    def __delitem__(self, key: Any) -> None:
        index = self.find_value_from_key(key)
        if self.hash_table[index]:
            del self.hash_table[index]
        else:
            raise KeyError("Key not found")

    def find_index(self, key: Any) -> int:
        hashed_ = hash(key)
        index = hashed_ % self.max_capacity
        if self.hash_table[index] and self.hash_table[index][0] == key:
            return index
        if self.hash_table[index]:
            while self.hash_table[index]:
                if index == self.max_capacity - 1:
                    index = 0
                    continue
                if self.hash_table[index][0] == key:
                    return index
                index += 1
        return index

    def find_value_from_key(self, key: Any) -> int:
        hashed_ = hash(key)
        index = hashed_ % self.max_capacity
        if not self.hash_table[index]:
            raise KeyError("Key doesn't exist")
        if self.hash_table[index][0] == key:
            return index
        while self.hash_table[index][0] != key:
            if index == self.max_capacity - 1:
                index = 0
                continue
            index += 1
            if not self.hash_table[index]:
                raise KeyError("Key doesn't exist")
        return index

    def resize_table(self) -> None:
        self.max_capacity *= 2
        self.threshold = self.max_capacity - (self.max_capacity * 2 // 3)
        old_hash_table = self.hash_table
        self.hash_table = [None] * self.max_capacity
        for item in old_hash_table:
            if not item:
                continue
            index = self.find_index(item[0])
            self.hash_table[index] = (item[0], item[1])

    def clear(self) -> None:
        self.hash_table = [None] * self.max_capacity
        return None

    def get(self, key: Any) -> Any:
        index = self.find_value_from_key(key)
        return self.hash_table[index][1]

    def pop(self, key: Any) -> Any:
        index = self.find_value_from_key(key)
        pair = self.hash_table[index]
        self.hash_table[index] = None
        return pair[1]

    def update(self, other: "Dictionary") -> None:
        for index, key in enumerate(other.hash_table):
            if not other.hash_table[index]:
                continue
            self.__setitem__(key[0], key[1])
        return

    def __iter__(self) -> Generator:
        return (
            key[0] for index, key in enumerate(self.hash_table)
            if self.hash_table[index]
        )
