from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.length = 8
        self.threshold = self.length * 2 // 3
        self.hash_table: list = [None] * self.length
        self.used_cells = 0

    def __setitem__(self, key: Any, value: Any) -> None:
        self.check_for_resize()

        index = self.index_from_key(key)
        while next_item := self.hash_table[index]:
            if next_item[0] == key:
                self.hash_table[index][1] = value
                return

            index = self.get_next_index(index)

        self.hash_table[index] = [key, value]
        self.used_cells += 1

    def check_for_resize(self) -> None:
        if self.used_cells + 1 > self.threshold:
            self.expand_table()

    def get_next_index(self, index: int) -> int:
        return index + 1 if index < self.length - 1 else 0

    def index_from_key(self, key: Any) -> int:
        return hash(key) % self.length

    def get(self, key: Any, default_value: Any = None) -> Any:
        if default_value:
            return self[key]
        else:
            return default_value

    def search_for_item(self, key: Any) -> Any:
        start_index = self.index_from_key(key)
        current_index = start_index
        while True:
            if not self.hash_table[current_index]:
                return None

            if (
                self.hash_table[current_index]
                and self.hash_table[current_index][0] == key
            ):
                return current_index

            current_index = self.get_next_index(current_index)
            if current_index == start_index:
                break

        return None

    def __getitem__(self, key: Any) -> None:
        found_index = self.search_for_item(key)
        if found_index is None:
            raise KeyError(f"{key}")
        else:
            return self.hash_table[found_index][1]

    def __len__(self) -> int:
        print(self.used_cells)
        return self.used_cells

    def __delitem__(self, key: Any) -> None:
        index = self.index_from_key(key)

        if not self.hash_table[index]:
            raise KeyError

        self.hash_table[index] = None
        self.used_cells -= 1

    def clear(self) -> None:
        self.hash_table: list = [None] * self.length
        self.used_cells = 0

    def expand_table(self) -> None:
        new_size = self.length * 2
        new_table = [None] * new_size

        for item in self.hash_table:
            if item:
                key, value = item
                index = hash(key) % new_size

                while new_table[index] is not None:
                    index = index + 1 if index < new_size - 1 else 0
                new_table[index] = [key, value]

        self.length = new_size
        self.hash_table = new_table
        self.threshold = new_size * 2 // 3

    def pop(self, key: Any) -> Any:
        value = self[key]
        del self[key]
        return value

    def __str__(self) -> str:
        key_value = [key_value for key_value in self.hash_table if key_value]
        return str(key_value)
