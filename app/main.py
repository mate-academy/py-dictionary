from typing import Any, Optional


class Dictionary:
    DELETED = object()
    _sentinel = object()

    def __init__(self) -> None:
        self.capacity = 8
        self.size = 0
        self.table = [None] * self.capacity

    def _find_slot(self, key: Any) -> Optional[int]:
        hash_key = hash(key) % self.capacity
        start_point = hash_key
        while True:
            if (
                self.table[hash_key] is None
                or self.table[hash_key] is self.DELETED
                or self.table[hash_key][0] == key
            ):
                return hash_key
            hash_key = (hash_key + 1) % self.capacity
            if hash_key == start_point:
                raise RuntimeError("Hash table is full")

    def _find_key(self, key: Any) -> Optional[int]:
        hash_key = hash(key) % self.capacity
        start_point = hash_key

        while True:
            if self.table[hash_key] is None:
                return None
            if (
                self.table[hash_key] is not self.DELETED
                and self.table[hash_key][0] == key
            ):
                return hash_key
            hash_key = (hash_key + 1) % self.capacity
            if hash_key == start_point:
                return None

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.size >= round(self.capacity * (2 / 3)):
            old_table = self.table
            self.capacity *= 2
            self.table = [None] * self.capacity
            self.size = 0
            for values in old_table:
                if values is not None and values is not self.DELETED:
                    self[values[0]] = values[1]
        hash_key = self._find_slot(key)

        if (
            self.table[hash_key] is None
            or self.table[hash_key] is self.DELETED
        ):
            self.size += 1
        self.table[hash_key] = (key, value, hash_key)

    def __getitem__(self, item: Any) -> Any:
        hash_item = self._find_key(item)
        if (
            hash_item is None
            or self.table[hash_item] is None
        ):
            raise KeyError(item)
        return self.table[hash_item][1]

    def __len__(self) -> int:
        return self.size

    def __delitem__(self, key: Any) -> None:
        hash_key = self._find_key(key)
        if (
                hash_key is None
                or self.table[hash_key] is None
        ):
            raise KeyError(key)
        if self.table[hash_key][0] == key:
            self.table[hash_key] = self.DELETED
            self.size -= 1

    def clear(self) -> None:
        self.table = [None] * self.capacity
        self.size = 0

    def get(self, key: Any, default: Any = None) -> Any:
        hash_key = self._find_key(key)
        if (
                hash_key is None
                or self.table[hash_key] is None
        ):
            return default
        if self.table[hash_key][0] == key:
            return self.table[hash_key][1]

    def pop(self, key: Any, default: Any = _sentinel) -> Any:
        hash_key = self._find_key(key)
        if hash_key is None:
            if default is self._sentinel:
                raise KeyError(key)
            return default

        value = self.table[hash_key][1]
        self.table[hash_key] = self.DELETED
        self.size -= 1
        return value

    def update(self, values: Any) -> None:
        for key, value in values.items():
            self[key] = value

    def items(self) -> list:
        list_items = list()
        for items in self.table:
            if items is not None and items is not self.DELETED:
                list_items.append((items[0], items[1]))
        return list_items

    def keys(self) -> list:
        keys_list = list()
        for keys in self.table:
            if keys is not None and keys is not self.DELETED:
                keys_list.append(keys[0])
        return keys_list

    def values(self) -> list:
        values_list = list()
        for values in self.table:
            if values is not None and values is not self.DELETED:
                values_list.append(values[1])
        return values_list

    def __repr__(self) -> str:
        dictionary = {
            key: value
            for slot in self.table
            if slot is not None
            and slot is not self.DELETED
            for key, value, _ in [slot]
        }
        return f"{dictionary}"

    def __iter__(self) -> Any:
        self.current = 0
        return self

    def __next__(self) -> Any:
        while self.current < self.capacity:
            item = self.table[self.current]
            self.current += 1
            if item is not None and item is not self.DELETED:
                return item[0]
        raise StopIteration
