from __future__ import annotations
from typing import Any, List, Hashable


class Dictionary:
    """
    remembers the order of item creation in Dictionary instance and allows
    iterating and printing items in the same order of creation
    """
    def __init__(self) -> None:
        self.length = 0
        self.hash_table: list = [None] * 8
        self.hash_table_len = 8
        self.load_factor = 2 / 3
        self.item_id = 0

    def __len__(self) -> int:
        return self.length

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hash_ = hash(key)
        index = hash_ % self.hash_table_len
        while self.hash_table[index]:
            if key == self.hash_table[index][0]:
                self.hash_table[index] = (
                    self.hash_table[index][0],
                    self.hash_table[index][1],
                    value,
                    self.hash_table[index][3]
                )
                return
            index = (index + 1) % self.hash_table_len
        self.hash_table[index] = (key, hash_, value, self.item_id)
        self.length += 1
        self.item_id += 1
        if self.length > self.hash_table_len * self.load_factor:
            self.resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = self.find_index(key)
        return self.hash_table[index][2]

    def resize(self) -> None:
        dup_hash_table = self.sort_items()
        self.hash_table_len *= 2
        self.hash_table = [None] * self.hash_table_len
        self.length = 0
        self.item_id = 0
        for el in dup_hash_table:
            self.__setitem__(el[0], el[2])

    @staticmethod
    def by_id(item: tuple[Hashable, int, Any, int]) -> int:
        return item[3]

    def sort_items(self) -> List[tuple[Hashable, int, Any, int]]:
        return sorted((item for item in self.hash_table if item),
                      key=self.by_id)

    def clear(self) -> None:
        self.__init__()

    def __delitem__(self, key: Hashable) -> None:
        index = self.find_index(key)
        self.hash_table[index] = None
        self.length -= 1

    def find_index(self, key: Hashable) -> int:
        hash_ = hash(key)
        index = hash_ % self.hash_table_len
        full_loop_index = index
        while True:
            if self.hash_table[index] and key == self.hash_table[index][0]:
                return index
            index = (index + 1) % self.hash_table_len
            if index == full_loop_index:
                raise KeyError(f"no item with key `{key}`")

    def get(self, key: Hashable, value: Any = None) -> Any:
        try:
            index = self.find_index(key)
        except KeyError:
            return value
        return self.hash_table[index][2]

    def pop(self, key: Hashable) -> Any:
        index = self.find_index(key)
        temporary_value = self.hash_table[index][2]
        self.hash_table[index] = None
        self.length -= 1
        return temporary_value

    def update(self, dictionary: Dictionary) -> None:
        sorted_items = dictionary.sort_items()
        for item in sorted_items:
            if item:
                self.__setitem__(item[0], item[2])

    def __iter__(self) -> Dictionary:
        """
        cool feature: remembers state of `dictionary` upon calling `__iter__`
        """
        self.dup_hash_table = self.hash_table[:]
        self.iter_count = 0
        self.sorted_items = self.sort_items()
        return self

    def __next__(self) -> Hashable:
        """
        cool feature: returns a RuntimeError if new items were added and/or
        items were deleted from `dictionary` during iteration, even when
        length stayed the same
        """
        if self.dup_hash_table != self.hash_table:
            raise RuntimeError("dictionary changed during iteration")
        if self.iter_count == self.length:
            raise StopIteration
        tmp_item = self.sorted_items[self.iter_count]
        self.iter_count += 1
        return tmp_item[0]

    def __str__(self) -> str:
        sorted_items = self.sort_items()
        string = []
        for item in sorted_items:
            string.append(f"{item[0]}: {item[2]}")
        return "{" + ", ".join(string) + "}"
