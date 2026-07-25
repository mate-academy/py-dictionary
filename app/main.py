from typing import Hashable, Any


class Dictionary:
    INITIAL_CAPACITY = 8
    LOAD_FACTOR = 2 / 3

    def __init__(self) -> None:
        self.capacity = self.INITIAL_CAPACITY
        self.length = 0
        self.hash_table = [None] * self.capacity

    @property
    def threshold(self) -> int:
        return int(self.capacity * self.LOAD_FACTOR)

    def __len__(self) -> int:
        return self.length

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.length == self.threshold:
            self._resize_table()

        hash_key = hash(key)
        index_item = hash_key % self.capacity
        while self.hash_table[index_item]:
            if (
                self.hash_table[index_item][0] == key
                and self.hash_table[index_item][1] == hash_key
            ):
                self.hash_table[index_item][2] = value
                return
            index_item = (index_item + 1) % self.capacity
        self.hash_table[index_item] = [key, hash_key, value]
        self.length += 1

    def __getitem__(self, key: Hashable) -> Any:
        hash_key = hash(key)
        item_index = hash_key % self.capacity
        if self.hash_table[item_index]:
            start_index = item_index
            while True:
                if (
                    self.hash_table[item_index][0] == key
                    and self.hash_table[item_index][1] == hash_key
                ):
                    return self.hash_table[item_index][2]
                item_index = (item_index + 1) % self.capacity
                if item_index == start_index:
                    break
        raise KeyError("Key not found")

    def _resize_table(self) -> None:
        old_table = self.hash_table

        self.capacity *= 2
        self.hash_table = [None] * self.capacity

        for item in old_table:
            if item is None:
                continue

            item_hash = item[1]
            item_index = item_hash % self.capacity
            while self.hash_table[item_index]:
                item_index = (item_index + 1) % self.capacity
            self.hash_table[item_index] = item
