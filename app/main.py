from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.hash_table: list = [None] * 8

    def __getitem__(
            self, key: Hashable
    ) -> None:
        hash_key = hash(key)
        index = hash_key % len(self.hash_table)

        if (
                self.hash_table[index]
                and self.hash_table[index][2] == hash_key
                and self.hash_table[index][0] == key
        ):
            return self.hash_table[index][1]
        else:
            for item in self.hash_table:
                if item and item[0] == key:
                    return item[1]

        raise KeyError

    def __setitem__(
            self,
            key: Hashable,
            value: Any
    ) -> None:
        if self.length > len(self.hash_table) * 2 / 3:
            self.extend_hash_table()

        hash_key = hash(key)
        item = (key, value, hash_key)
        index = hash_key % len(self.hash_table)

        if self.hash_table[index] and self.hash_table[index][0] == key:
            self.hash_table[index] = (key, value, hash_key)
        else:
            is_key_exists = False

            for i in range(len(self.hash_table)):
                if self.hash_table[i] and self.hash_table[i][0] == key:
                    self.hash_table[i] = item
                    is_key_exists = True

            if not is_key_exists:

                while self.hash_table[index]:
                    index = (
                        index + 1
                        if index != len(self.hash_table) - 1
                        else 0
                    )

                self.hash_table[index] = item
                self.length += 1

    def extend_hash_table(self) -> None:
        extending = [None] * len(self.hash_table)
        self.hash_table += extending

        for i in range(len(self.hash_table) // 2):
            if self.hash_table[i]:
                self.__setitem__(self.hash_table[i][0], self.hash_table[i][1])

    def __len__(self) -> int:
        return self.length
