from typing import Any


class Dictionary:

    def __init__(self, capacity: int = 8) -> None:
        # Початкова місткість таблиці
        self.capacity = capacity
        # Поточна кількість елементів
        self.count_el = 0
        # Список порожніх списків (вузлів хеш-таблиці)
        self.table = [[] for _ in range(capacity)]
        self.load_factor = 0.66

    def __setitem__(self, key: Any, value: Any) -> None:

        index_to_save_in_table = hash(key) % self.capacity

        for indx, (k, v) in enumerate(self.table[index_to_save_in_table]):
            if k == key:
                self.table[index_to_save_in_table][indx] = (key, value)
                return

        self.table[index_to_save_in_table].append((key, value))
        self.count_el += 1

        if self.count_el / self.capacity > self.load_factor:
            self._resize()

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_table = [[] for _ in range(new_capacity)]

        for bucket in self.table:
            for k, v in bucket:
                new_index = hash(k) % new_capacity
                new_table[new_index].append((k, v))

        self.capacity = new_capacity
        self.table = new_table

    def __getitem__(self, key: Any) -> Any:

        index = hash(key) % self.capacity
        bucket = self.table[index]

        for k, v in bucket:
            if k == key:
                return v

        raise KeyError(f"Key '{key}' not found in the dictionary")

    def __len__(self) -> int:
        return self.count_el

    def clear(self) -> None:
        self.count_el = 0
        self.table = [[] for _ in range(self.capacity)]

    def __delitem__(self, key: Any) -> None:

        index = hash(key) % self.capacity
        bucket = self.table[index]

        for i, (k, _) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.count_el -= 1
                return

        raise KeyError(f"Key '{key}' not found in the dictionary")

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def __contains__(self, key: Any) -> bool:

        index = hash(key) % self.capacity
        bucket = self.table[index]

        for k, v in bucket:
            if k == key:
                return True
        return False

    def keys(self) -> list:
        return [k for bucket in self.table for k, _ in bucket]

    def values(self) -> list:
        return [v for bucket in self.table for _, v in bucket]

    def items(self) -> list:
        return [(k, v) for bucket in self.table for k, v in bucket]
