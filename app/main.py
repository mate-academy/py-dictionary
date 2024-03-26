from typing import Hashable, Any


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.hash_table: list = [None] * 8
        self.load_hash_table = 2 / 3

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hash_ = hash(key)
        item_hashing = hash_ % len(self.hash_table)
        while 1:
            if not self.hash_table[item_hashing]:
                if (self.length + 1 > self.load_hash_table
                        * len(self.hash_table)):
                    self.resize()
                    item_hashing = hash_ % len(self.hash_table)
                    continue
                self.length += 1
                self.hash_table[item_hashing] = (key, hash_, value)
                break
            elif self.hash_table[item_hashing][0] == key:
                self.hash_table[item_hashing] = (key, hash_, value)
                break
            item_hashing = (item_hashing + 1) % len(self.hash_table)

    def __getitem__(self, item: Hashable) -> Any:
        hash_item = hash(item) % len(self.hash_table)
        checked = 0
        while checked < len(self):
            if (self.hash_table[hash_item]
                    and self.hash_table[hash_item][0] == item):
                return self.hash_table[hash_item][2]
            hash_item = (hash_item + 1) % len(self.hash_table)
            checked += 1
        raise KeyError

    def __len__(self) -> int:
        return self.length

    def resize(self) -> None:
        old_table = self.hash_table
        self.hash_table = [None] * len(self.hash_table) * 2
        self.length = 0
        [self.__setitem__(item[0], item[2]) for item in old_table if item]
