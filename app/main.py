from typing import Generator


class Dictionary:
    def __init__(self) -> None:
        self._size = 8
        self._threshold = 0.3
        self._table: list[list] = [[] for _ in range(self._size)]
        self._resize_const = 2

    def print_table(self) -> None:
        print(self._table)

    def __getitem__(self, key: any) -> all:
        hash_key = hash(key)
        table_index = hash_key % self._size

        for _ in range(self._size):
            entry = self._table[table_index]
            if entry and entry[1] == key:
                return entry[0]
            table_index = next(self._gen_next_slot(table_index))

        raise KeyError(f"Key {key} not found")

    def __setitem__(self, key: any, value: any) -> None:
        if isinstance(key, (list, set, dict)):
            raise KeyError

        if len(self) >= self._threshold * self._size:
            self._resize_table()

        hash_key = hash(key)
        table_index = hash_key % self._size

        for _ in range(self._size):
            if not self._table[table_index]:
                self._table[table_index] = [value, key]
                return
            else:
                if self._table[table_index][1] == key:
                    self._table[table_index] = [value, key]
                    return

                table_index = next(self._gen_next_slot(table_index))

    def _resize_table(self) -> None:
        old_size = self._size
        self._size *= self._resize_const
        new_table: list[list] = [[] for _ in range(self._size)]

        for index in range(old_size):
            if self._table[index]:
                hash_key = hash(self._table[index][1])
                new_table_index = hash_key % self._size

                for _ in range(self._size):
                    if not new_table[new_table_index]:
                        new_table[new_table_index] = self._table[index]
                        break
                    else:
                        new_table_index = (
                            next(self._gen_next_slot(new_table_index)))

        self._table = new_table

    def _gen_next_slot(self, start_index: int) -> Generator[int, None, None]:
        index = start_index

        while True:
            index = (index + 1) % self._size
            yield index

    def __len__(self) -> int:
        length_table = 0
        for index in range(self._size):
            if self._table[index]:
                length_table += 1

        return length_table
