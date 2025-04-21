import copy
from typing import Any, Iterator


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.hash_table: list = [None] * 8

    def __len__(self) -> int:
        return self.length

    def __getitem__(self, item: Any) -> Any:
        hash_key = hash(item)
        key_index = hash_key % len(self.hash_table)

        while True:
            if self.hash_table[key_index] is None:
                raise KeyError(item)

            stored_hash, stored_key, stored_value = self.hash_table[key_index]

            if stored_key == item and stored_hash == hash_key:
                return stored_value

            key_index = (key_index + 1) % len(self.hash_table)

    def __setitem__(self, key: Any, value: Any) -> None:
        if len(self) == int(len(self.hash_table) * 2 / 3):
            self.resize()

        hash_key = hash(key)
        key_index = hash_key % len(self.hash_table)

        while True:
            if self.hash_table[key_index] is None:
                self.hash_table[key_index] = [hash_key, key, value]
                self.length += 1
                return

            existing_hash, existing_key, _ = self.hash_table[key_index]
            if existing_hash == hash_key and existing_key == key:
                self.hash_table[key_index][2] = value
                return

            key_index = (key_index + 1) % len(self.hash_table)

    def resize(self) -> None:
        temp_table = copy.deepcopy(self.hash_table)
        self.hash_table = [None] * (len(temp_table) * 2)
        self.length = 0

        for item in temp_table:
            if item is not None:
                self[item[1]] = item[2]

    def get(self, item: Any, option_oper: None = None) -> Any:
        hash_key = hash(item)
        key_index = hash_key % len(self.hash_table)

        while True:
            if self.hash_table[key_index] is None:
                return option_oper

            stored_hash, stored_key, stored_value = self.hash_table[key_index]

            if stored_key == item and stored_hash == hash_key:
                return stored_value

            key_index = (key_index + 1) % len(self.hash_table)

    def __iter__(self) -> Iterator[Any]:
        self.iter_index = 0
        return self

    def __next__(self) -> Any:

        while self.iter_index < len(self.hash_table):
            current_items = self.hash_table[self.iter_index]
            self.iter_index += 1
            if current_items is not None:

                return current_items[1]

        raise StopIteration

    def clear(self) -> None:
        self.hash_table = [None] * len(self.hash_table)
        self.length = 0

    def __delitem__(self, key: Any) -> None:
        hash_key = hash(key)
        key_index = hash_key % len(self.hash_table)

        while True:
            if self.hash_table[key_index] is None:
                raise KeyError(key)

            stored_hash, stored_key, stored_value = self.hash_table[key_index]
            if stored_key == key and stored_hash == hash_key:
                break

        self.hash_table[key_index] = None
        self.length -= 1

        next_index = (key_index + 1) % len(self.hash_table)
        while self.hash_table[next_index] is not None:
            temp_item = self.hash_table[next_index]
            self.hash_table[next_index] = None
            self.length -= 1

            self[temp_item[1]] = temp_item[2]

            next_index = (next_index + 1) % len(self.hash_table)

    def pop(self, key: Any, default: Any = None) -> None:
        hash_key = hash(key)
        key_index = hash_key % len(self.hash_table)

        while True:
            if self.hash_table[key_index] is None:
                if default is not None:
                    return default
                raise KeyError(key)

            stored_hash, stored_key, stored_value = self.hash_table[key_index]

            if stored_key == key and stored_hash == hash_key:
                self.hash_table[key_index] = None
                self.length -= 1
                next_index = (key_index + 1) % len(self.hash_table)
                while self.hash_table[next_index] is not None:
                    (next_hash,
                     next_key,
                     next_value) = self.hash_table[next_index]
                    self.hash_table[next_index] = None
                    self.length -= 1
                    self[next_key] = next_value
                    next_index = (next_index + 1) % len(self.hash_table)
                return stored_value

            key_index = (key_index + 1) % len(self.hash_table)

    def update(self, other: Any, **kwargs) -> None:
        if isinstance(other, dict):
            for key, value in other.items():
                self[key] = value
        else:
            for key, value in other:
                self[key] = value
        for key, value in kwargs.items():
            self[key] = value

    def __str__(self) -> str:
        result = "{"
        finish_str = "}"
        items = []

        for item in self.hash_table:
            if item is not None:
                _, key, value = item
                items.append(f"{key}: {value}")
        result += ", ".join(items) + finish_str

        return result
