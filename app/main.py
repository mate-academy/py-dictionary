from typing import Any


class Item:
    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.value = value
        self.hash_key = hash(self.key)


class Dictionary:
    def __init__(self) -> None:
        self.table = [None] * 8
        self.table_size = 8
        self.load_factor = round((2 * self.table_size) / 3)

    def __setitem__(self, key: Any, value: Any) -> None:
        hash_key = hash(key)
        index = hash_key % self.table_size
        if self.table[index] is None:
            self.table[index] = Item(key, value)
            return
        elif self.table[index].key == key:
            self.table[index].value = value
            return
        key_status, collision_index = self.__check_tabel__(key, index)
        if key_status:
            self.table[collision_index].value = value
        else:
            item = Item(key, value)
            self.table = Dictionary.__collision__(self.table, item, index)
        if (self.__len__()) >= self.load_factor:
            self.__resize__()

    def __getitem__(self, key: Any) -> Any:
        hash_key = hash(key)
        index = hash_key % self.table_size
        if self.table[index] is None:
            raise KeyError
        elif self.table[index].key == key:
            return self.table[index].value
        key_status, collision_index = self.__check_tabel__(key, index)
        if key_status:
            return self.table[collision_index].value
        raise KeyError

    def __check_tabel__(self, key: Any, start_index: int) -> tuple:
        index = start_index + 1
        while index <= self.table_size - 1:
            if self.table[index] is None:
                pass
            elif self.table[index].key == key:
                return True, index
            index += 1
        index = 0
        while index != start_index:
            if self.table[index] is None:
                pass
            elif self.table[index].key == key:
                return True, index
            index += 1
        return False, None

    def __resize__(self) -> None:
        self.table_size = self.table_size * 2
        self.load_factor = round((2 * self.table_size) / 3)
        new_table = [None] * self.table_size
        exist_items = [
            item
            for item in self.table
            if item is not None
        ]
        for item in exist_items:
            index = item.hash_key % self.table_size
            if new_table[index] is None:
                new_table[index] = item
                continue
            else:
                new_table = Dictionary.__collision__(new_table, item, index)
        self.table = new_table

    @staticmethod
    def __collision__(table: list, item: Any, index: int) -> list:
        index += 1
        while index <= len(table) - 1:
            if table[index] is None:
                table[index] = item
                return table
            index += 1
        index = 0
        while True:
            if table[index] is None:
                table[index] = item
                return table
            index += 1

    def __len__(self) -> int:
        return len(
            [item
             for item in self.table
             if item is not None
             ])
