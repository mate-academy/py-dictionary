from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.count_el = 0
        self.hash_table: list = [[] for _ in range(self.capacity)]
        self.load_factor = 0.66

    def __setitem__(self, key: Any, value: Any) -> None:
        index_to_save = hash(key) % self.capacity
        for index, (k, v) in enumerate(self.hash_table[index_to_save]):
            if k == key:
                self.hash_table[index_to_save][index] = (key, value)
                return
        self.hash_table[index_to_save].append((key, value))
        self.count_el += 1
        if self.count_el / self.capacity > self.load_factor:
            self._resize()

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_hash_table = [[] for _ in range(new_capacity)]
        for bucket in self.hash_table:
            for k, v in bucket:
                new_index = hash(k) % new_capacity
                new_hash_table[new_index].append((k, v))
        self.capacity = new_capacity
        self.hash_table = new_hash_table

    def __getitem__(self, item: Any) -> Any:
        index = hash(item) % self.capacity
        for key, value in self.hash_table[index]:
            if key == item:
                return value
        raise KeyError(f"Key '{item}' not found in the dictionary")

    def __len__(self) -> int:
        return self.count_el

    def clear(self) -> None:
        self.hash_table = [[] for _ in range(self.capacity)]
        self.count_el = 0

    def __delitem__(self, key: Any) -> None:
        index = hash(key) % self.capacity
        for indx, (k, v) in enumerate(self.hash_table[index]):
            if k == key:
                del self.hash_table[index][indx]
                self.count_el -= 1
                return
        raise KeyError(f"Key '{key}' not found in the dictionary")

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Any, default: Any = None) -> Any:
        index = hash(key) % self.capacity
        for indx, (k, v) in enumerate(self.hash_table[index]):
            if k == key:
                del self.hash_table[index][indx]
                self.count_el -= 1
                return v
        if default is not None:
            return default
        raise KeyError
