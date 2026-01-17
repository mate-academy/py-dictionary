from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.hash_table: list = [None] * 8
        self.hash_table_size = 8
        self.load_factor = 2 / 3
        self.breakpoint = int(self.hash_table_size * self.load_factor)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        flag = self.is_new_key(key)

        if flag:
            try:
                hash_key = hash(key)
            except TypeError:
                raise
            node = (key, hash_key, value)

            if self.breakpoint == self.length:
                self.resize_hash_table()

            place_for_element = self.find_free_slot(
                self.hash_table, node
            )
            self.hash_table[place_for_element] = node
            self.length += 1
            return

        for index, elem in enumerate(self.hash_table):
            if elem is not None:
                if elem[0] == key:
                    self.hash_table[index] = (elem[0], elem[1], value)

    def __getitem__(self, item: Hashable) -> Any:
        for node in self.hash_table:
            if isinstance(node, tuple) and node[0] == item:
                return node[2]
        raise KeyError(f"{item}")

    def __len__(self) -> int:
        return self.length

    def find_free_slot(
        self, source_list: list, element: tuple
    ) -> int:
        hash_key = element[1]
        initial_place = hash_key % self.hash_table_size

        while True:
            if source_list[initial_place] is None:
                return initial_place

            if source_list[initial_place][0] == element[0]:
                return initial_place

            if initial_place == self.hash_table_size - 1:
                initial_place = 0
                continue
            initial_place += 1

    def resize_hash_table(self) -> None:
        self.hash_table_size *= 2
        self.breakpoint = int(self.hash_table_size * self.load_factor)
        hash_table_temp = [None] * self.hash_table_size
        for nod in self.hash_table:
            if nod:
                place_after_resizing = self.find_free_slot(
                    hash_table_temp, nod
                )
                hash_table_temp[place_after_resizing] = nod
        self.hash_table = hash_table_temp

    def is_new_key(self, value: Hashable) -> bool:
        for nod in self.hash_table:
            if isinstance(nod, tuple) and nod[0] == value:
                return False
        return True

    def clear(self) -> None:
        self.hash_table_size = 8
        self.breakpoint = int(self.hash_table_size * self.load_factor)
        self.hash_table = [None] * self.hash_table_size
        self.length = 0

    def __delitem__(self, key: Any) -> None:
        for index, elem in enumerate(self.hash_table):
            if elem is not None and elem[0] == key:
                self.hash_table[index] = None
                self.length -= 1
                return
        raise KeyError(f"{key} not found in the dictionary")
