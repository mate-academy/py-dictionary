from typing import Any, Hashable


class Dictionary:

    LOAD_FACTOR = 2 / 3

    def __init__(self) -> None:
        self.length = 0
        self.hash_table: list = [None] * 8

    def __setitem__(self, key: Hashable, value: Any) -> None:

        hash_cell = hash(key) % len(self.hash_table)

        if (
                self.hash_table[hash_cell]
                and self.hash_table[hash_cell].key == key
        ):
            self.hash_table[hash_cell].value = value
            return
        if (
                self.hash_table[hash_cell]
                and self.hash_table[hash_cell].key != key
        ):
            for item in self.hash_table:
                if item and item.key == key:
                    item.value = value
                    return
        hash_cell = self.get_free_cell(hash_cell)
        self.add_new_item(hash_cell, key, value)

    def __getitem__(self, key: Hashable) -> Any:
        for item in self.hash_table:
            if item and item.key == key:
                return item.value
        raise KeyError(f"Key '{key}' not found")

    def __len__(self) -> int:
        return self.length

    def get_free_cell(self, hash_cell: int) -> int:
        while self.hash_table[hash_cell]:
            hash_cell = (hash_cell + 1) % len(self.hash_table)
        return hash_cell

    def resize_hash_table(self) -> None:
        old_hash_table = self.hash_table

        length_resized_hash_table = len(self.hash_table) * 2
        self.hash_table = [None] * length_resized_hash_table

        for item in old_hash_table:
            if item:
                hash_cell = hash(item.key) % length_resized_hash_table
                if self.hash_table[hash_cell]:
                    hash_cell = self.get_free_cell(hash_cell)
                self.hash_table[hash_cell] = item

    def add_new_item(self, hash_cell: int, key: Hashable, value: Any) -> None:
        if len(self) == int(self.LOAD_FACTOR * len(self.hash_table)):
            self.resize_hash_table()
            hash_cell = hash(key) % len(self.hash_table)
            if self.hash_table[hash_cell]:
                hash_cell = self.get_free_cell(hash_cell)
        self.hash_table[hash_cell] = ItemDictionary(key, value)
        self.length += 1

    def clear(self) -> None:
        for item in self.hash_table:
            if item:
                self.__delitem__(item.key)
        self.__init__()

    def __delitem__(self, key: Hashable) -> None:
        for item in self.hash_table:
            if item and item.key == key:
                index_ = self.hash_table.index(item)
                del item
                self.hash_table[index_] = None
                self.length -= 1
                break

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            get_value = self.__getitem__(key)
        except KeyError:
            return default
        return get_value

    def pop(self, key: Hashable) -> Any:
        get_value = self.get(key)
        self.__delitem__(key)
        return get_value

    def update(self, other: Any) -> None:
        for item in other.hash_table:
            if item:
                self.__setitem__(item.key, item.value)

    def __iter__(self) -> Any:
        for item in self.hash_table:
            if item:
                yield item.key


class ItemDictionary:
    def __init__(self, key: Hashable, value: Any) -> None:
        self.key = key
        self.value = value
