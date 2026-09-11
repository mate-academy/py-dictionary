from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.hash_table = [None] * 8

    def __len__(self) -> int:
        return self.length

    def __setitem__(self, key: Hashable, value: Any) -> None:
        key_hash = hash(key)
        index = key_hash % len(self.hash_table)

        while True:
            node = self.hash_table[index]

            if node is None:
                filled = (self.length + 1) / len(self.hash_table)

                if filled >= 2 / 3:
                    self._resize()
                    self[key] = value
                    return

                self.hash_table[index] = [key, key_hash, value]
                self.length += 1
                return

            elif node[0] == key:
                node[2] = value
                return

            else:
                index = (index + 1) % len(self.hash_table)

    def __getitem__(self, key: Hashable) -> Any:
        key_hash = hash(key)
        index = key_hash % len(self.hash_table)

        while True:
            node = self.hash_table[index]

            if node is None:
                raise KeyError(f"Key not found {key!r}")

            elif node[0] == key:
                return node[2]

            else:
                index = (index + 1) % len(self.hash_table)

    def _resize(self) -> None:
        old_table = self.hash_table
        self.hash_table = [None] * (len(old_table) * 2)
        self.length = 0

        for node in old_table:
            if node is not None:
                self[node[0]] = node[2]
