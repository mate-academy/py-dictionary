from typing import Any


class Dictionary:

    def __init__(self, capacity: int = 8, load_factor: float = 2 / 3) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.hash_table: list = [None] * capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        hash_key = hash(key)
        index = hash_key % self.capacity

        while True:
            if self.hash_table[index]:
                if self.hash_table[index][0] == key and \
                        self.hash_table[index][2] == hash_key:
                    self.hash_table[index][1] = value
                    break

            elif self.hash_table[index] is None:
                self.hash_table[index] = [key, value, hash_key]
                break

            index = (index + 1) % self.capacity

        if len(self) > self.capacity * self.load_factor:
            self.resize()

    def __getitem__(self, key: Any) -> Any:
        hash_key = hash(key)
        index = hash_key % self.capacity
        while True:
            if self.hash_table[index]:
                if self.hash_table[index][0] == key and \
                        self.hash_table[index][2] == hash_key:
                    return self.hash_table[index][1]
            else:
                break

            index = (index + 1) % self.capacity

        raise KeyError(f"Invalid key: {key}")

    def __len__(self) -> int:
        return len([elem for elem in self.hash_table if elem])

    def resize(self) -> None:
        capacity_new = 2 * self.capacity
        hash_table_new = [None] * capacity_new

        for cell in self.hash_table:
            if cell:
                index2 = hash(cell[0]) % capacity_new

                while True:
                    if hash_table_new[index2] is None:
                        hash_table_new[index2] = [cell[0], cell[1], cell[2]]
                        break

                    index2 = (index2 + 1) % capacity_new

        self.hash_table = hash_table_new
        self.capacity = capacity_new
