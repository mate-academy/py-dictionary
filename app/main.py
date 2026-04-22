from typing import Any


class Dictionary:
    DELETED = object()

    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.hash_table: list = [None] * self.capacity

    def __len__(self) -> int:
        return self.length

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.length >= len(self.hash_table) * 2 / 3:
            self.recalculate_hashes()

        hash_key = hash(key)
        index = hash_key % len(self.hash_table)
        first_deleted_index = None

        while True:
            entry = self.hash_table[index]

            if entry is None:
                target_index = first_deleted_index \
                    if first_deleted_index is not None \
                    else index
                self.hash_table[target_index] = (key, hash_key, value)
                self.length += 1
                return

            if entry is self.DELETED:
                if first_deleted_index is None:
                    first_deleted_index = index
            elif entry[0] == key:
                self.hash_table[index] = (key, hash_key, value)
                return

            index = (index + 1) % len(self.hash_table)

    def __getitem__(self, key: Any) -> Any:
        hash_key = hash(key)
        index = hash_key % len(self.hash_table)
        start_index = index

        while self.hash_table[index] is not None:
            entry = self.hash_table[index]
            if entry is not self.DELETED and entry[0] == key:
                return entry[2]

            index = (index + 1) % len(self.hash_table)

            if index == start_index:
                break

        raise KeyError(f"Key {key} not found.")

    def __delitem__(self, key: Any) -> None:
        hash_key = hash(key)
        index = hash_key % len(self.hash_table)
        start_index = index

        while self.hash_table[index] is not None:
            entry = self.hash_table[index]
            if entry is self.DELETED:
                pass
            elif entry[0] == key:
                self.hash_table[index] = self.DELETED
                self.length -= 1
                return

            index = (index + 1) % len(self.hash_table)

            if index == start_index:
                break

        raise KeyError(f"Key {key} not found.")

    def __iter__(self) -> Any:
        for entry in self.hash_table:
            if entry is not None and entry is not self.DELETED:
                yield entry[0]

    def clear(self) -> None:
        self.__init__()

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Any, default: Any = None) -> Any:
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            return default

    def recalculate_hashes(self) -> None:
        old_table = self.hash_table
        self.capacity = len(old_table) * 2
        self.hash_table = [None] * self.capacity
        self.length = 0

        for entry in old_table:
            if entry is not None and entry is not self.DELETED:
                key, _, value = entry
                self.__setitem__(key, value)
