from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.hash_table: list[None | tuple[Hashable, hash, Any]] = [None] * 8
        self.load_factor = 2 / 3
        self.capacity = 2

    @staticmethod
    def add_item_to_table(
            table: list[None | tuple[Hashable, hash, Any]],
            key: Hashable,
            value: Any
    ) -> None:
        hash_ = hash(key)
        index = hash_ % (len(table) - 1)
        while True:
            if not table[index] or table[index][0] == key:
                table[index] = key, hash_, value
                break
            index += 1
            if index == len(table):
                index = 0

    def rehash(self) -> None:
        new_hash_table = [None] * len(self.hash_table) * self.capacity

        for item in self:
            self.add_item_to_table(
                new_hash_table,
                item,
                self.__getitem__(item)
            )

        self.hash_table = new_hash_table

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if len(self) > self.load_factor * len(self.hash_table):
            self.rehash()
        if key not in self:
            self.length += 1
        self.add_item_to_table(self.hash_table, key, value)

    def __getitem__(self, item: Hashable) -> Any:
        if item not in self:
            raise KeyError
        index = hash(item) % (len(self.hash_table) - 1)
        while True:
            if self.hash_table[index] and self.hash_table[index][0] == item:
                return self.hash_table[index][2]
            index += 1
            if index == len(self.hash_table):
                index = 0

    def __delitem__(self, key: Hashable) -> None:
        if key not in self:
            raise KeyError
        index = hash(key) % (len(self.hash_table) - 1)
        while True:
            if self.hash_table[index] and self.hash_table[index][0] == key:
                self.hash_table[index] = None
                self.length -= 1
                break
            index += 1
            if index == len(self.hash_table):
                index = 0

    def clear(self) -> None:
        self.hash_table = [None] * len(self.hash_table)
        self.length = 0

    def get(self, key: Hashable, value: Any) -> Any:
        if key in self:
            return self.__getitem__(key)
        return value

    def pop(self, key: Hashable) -> Any:
        output = self.__getitem__(key)
        self.__delitem__(key)
        return output

    def update(self, other: dict) -> None:
        for key in other:
            self.__setitem__(key, other.__getitem__(key))

    def __iter__(self) -> iter:
        return iter(item[0] for item in self.hash_table if item)

    def __len__(self) -> int:
        return self.length
