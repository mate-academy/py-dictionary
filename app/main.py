from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.size = 8
        self.load_factor = 0.67
        self.hash_table = [None] * self.size

    def __len__(self) -> int:
        return self.length

    def __getitem__(self, key: Hashable) -> Hashable:
        slot_index = hash(key) % self.size
        for slot in (
                self.hash_table[slot_index:] + self.hash_table[:slot_index]
        ):
            if slot and key == slot[0]:
                return slot[2]
        raise KeyError

    def __setitem__(self, key: Hashable, value: Any) -> None:
        slot_index = hash(key) % self.size
        while True:
            if not self.hash_table[slot_index]:
                self.length += 1
                break
            if self.hash_table[slot_index][0] == key:
                break
            slot_index = (slot_index + 1) % self.size

        self.hash_table[slot_index] = (key, hash(key), value)
        if self.size * self.load_factor <= self.length:
            self.resize()

    def resize(self) -> None:
        temp_hash_table = self.hash_table
        self.length = 0
        self.size *= 2
        self.hash_table = [None] * self.size

        for index, slot in enumerate(temp_hash_table):
            if slot:
                self.__setitem__(slot[0], slot[2])

    def clear(self) -> None:
        self.__init__()
