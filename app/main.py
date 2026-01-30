from typing import Self


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = 0.66
        self.count_items = 0
        self.table = [
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ]

    def __setitem__(self, key: any, value: any) -> None:
        hash_key = hash(key)
        start_index = hash_key % self.capacity
        slot = self.__find_slot(key, start_index)
        if slot is None:
            raise RuntimeError("No free slot found")

        self.__write_slot(slot, hash_key, key, value)
        if self.capacity * self.load_factor < self.count_items:
            self.__resize()

    def __find_slot(
        self: Self,
        key: any,
        start_index: int,
    ) -> int | None:
        start_index %= self.capacity
        for step in range(self.capacity):
            index = (start_index + step) % self.capacity
            if self.table[index] is None or self.table[index][1] == key:
                return index
        return None

    def __write_slot(
        self: Self,
        index: int,
        hash_key: int,
        key: any,
        value: any,
    ) -> None:
        if self.table[index] is None:
            self.count_items += 1
        self.table[index] = [hash_key, key, value]

    def __resize(self: Self) -> None:
        old_table = self.table
        self.table = [None for _ in range(self.capacity * 2)]
        for item in old_table:
            hash_key = item[0]
            start_index = hash_key % self.capacity
            slot = self.__find_slot(item[1], start_index)
            if slot is None:
                raise RuntimeError("No free slot found")

            self.__write_slot(slot, hash_key, item[1], item[2])
