from typing import Hashable, Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = int((self.capacity * 2) // 3)
        self.load_slots = 0
        self.free_slots = self.create_hash_table()

    def create_hash_table(self) -> list:
        return [[] for _ in range(self.capacity)]

    def resize(self) -> None:
        new_hash_table = self.free_slots
        self.load_slots = 0
        self.capacity *= 2
        self.load_factor = int((self.capacity * 2) // 3)
        self.free_slots = self.create_hash_table()

        for items in new_hash_table:
            if items:
                self.__setitem__(items[0], items[2])

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.load_slots == self.load_factor:
            self.resize()
        hashed_key = hash(key)
        index = hashed_key % self.capacity
        while True:
            if len(self.free_slots[index]) == 0:
                self.free_slots[index] = [key, hashed_key, value]
                self.load_slots += 1
                return
            elif self.free_slots[index][0] == key\
                    and self.free_slots[index][1] == hashed_key:
                self.free_slots[index][2] = value
                return

            index = (index + 1) % self.capacity

    def __getitem__(self, input_key: Hashable) -> Any:
        hashed_key = hash(input_key)
        index = hashed_key % self.capacity
        while self.load_factor != self.load_slots:
            if len(self.free_slots[index]) == 0:
                raise KeyError
            if input_key == self.free_slots[index][0]:
                return self.free_slots[index][2]
            else:
                index = (index + 1) % self.capacity
        raise KeyError

    def __len__(self) -> int:
        return self.load_slots

    def __delitem__(self, key: Hashable) -> Any:
        hashed_key = hash(key)
        index = hashed_key % self.capacity
        while True:
            if len(self.free_slots[index]) != 0 and\
                    self.free_slots[index][1] == hashed_key\
                    and key == self.free_slots[index][0]:
                self.free_slots[index][0] = hashed_key
                self.load_slots -= 1
                break
            else:
                index = (index + 1) % self.capacity
