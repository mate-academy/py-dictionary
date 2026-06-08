from typing import Any


class DictionaryItem:
    def __init__(
        self,
        key: Any,
        key_hash: int,
        value: Any
    ) -> None:
        self.key = key
        self.hash = key_hash
        self.value = value


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.table = [None] * self.capacity
        self.length = 0
        self.tombstone = DictionaryItem(None, None, None)

    def __setitem__(self, key: Any, value: Any) -> None:
        key_hash = hash(key)
        index = key_hash % self.capacity

        while self.table[index] is not None:
            if (self.table[index] is not self.tombstone
                    and self.table[index].key == key):
                self.table[index].value = value
                return
            index = (index + 1) % self.capacity

        self.table[index] = DictionaryItem(key, key_hash, value)
        self.length += 1

        if self.length / self.capacity >= 0.7:
            self._resize()

    def _resize(self) -> None:
        old_table = self.table

        self.capacity *= 2
        self.length = 0
        self.table = [None] * self.capacity

        for node in old_table:
            if node is not None and node is not self.tombstone:
                self.__setitem__(node.key, node.value)

    def __getitem__(self, key: Any) -> Any:
        index = hash(key) % self.capacity

        while self.table[index] is not None:
            if (self.table[index] is not self.tombstone
                    and self.table[index].key == key):
                return self.table[index].value

            index = (index + 1) % self.capacity

        raise KeyError(f"Key '{key}' not found in Dictionary.")

    def __len__(self) -> int:
        return self.length

    def __delitem__(self, key: Any) -> None:
        index = hash(key) % self.capacity

        while self.table[index] is not None:
            if (self.table[index] is not self.tombstone
                    and self.table[index].key == key):
                self.table[index] = self.tombstone
                self.length -= 1
                return
            index = (index + 1) % self.capacity
        raise KeyError(f"Key '{key}' not found.")
