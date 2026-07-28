from typing import Any


class Dictionary:
    def _inc_cell(self, _cell: int) -> int:
        cell = _cell
        if cell == self.len_hash_table - 1:
            cell = 0
        else:
            cell += 1
        return cell

    def _check_len(self) -> None:
        if self.len > int(self.len_hash_table * 2 / 3):
            self.len_hash_table *= 2
            new_hash_table = [
                [None, None, None] for _ in range(self.len_hash_table)
            ]
            for each in self.hash_table:
                if each[0] is not None:
                    new_cell = each[1] % self.len_hash_table
                    while new_hash_table[new_cell][0] is not None:
                        new_cell = self._inc_cell(new_cell)
                    new_hash_table[new_cell] = each[:]
            self.hash_table = new_hash_table

    def __setitem__(self, key: Any, value: Any) -> None:
        the_hash = hash(key)
        cell = the_hash % self.len_hash_table
        while True:
            if self.hash_table[cell][0] is not None:
                if (
                    self.hash_table[cell][0] == key
                    and self.hash_table[cell][1] == the_hash
                ):
                    self.hash_table[cell][2] = value
                    break
                else:
                    cell = self._inc_cell(cell)
            else:
                self.hash_table[cell] = [key, the_hash, value]
                self.len += 1
                self._check_len()
                break

    def __getitem__(self, key: Any) -> Any:
        # Starting point
        cell = hash(key) % self.len_hash_table
        # First key check just in case
        if self.hash_table[cell][0] != key:
            starting_point = cell
            while True:
                cell = self._inc_cell(cell)
                if cell == starting_point:
                    raise KeyError(f"No {key} key found!")
                if (
                    self.hash_table[cell][0] == key
                    and self.hash_table[cell][1] == hash(key)
                ):
                    break
        return self.hash_table[cell][2]

    def __len__(self) -> int:
        return self.len

    def __init__(self) -> None:
        self.len = 0
        self.hash_table = [[None, None, None] for _ in range(8)]
        self.len_hash_table = 8
