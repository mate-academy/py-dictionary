from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.size = 0
        self.capacity = 8
        self.table: list = [None] * self.capacity

    def _get_index(self, key: Any) -> int:
        hask_key = hash(key)
        result_index = hask_key % self.capacity
        return result_index

    def __setitem__(self, key: Any, value: Any) -> None:
        index_of_key = self._get_index(key)
        key_hash = hash(key)
        if self.table[index_of_key] is not None:
            if key == self.table[index_of_key][0]:
                self.table[index_of_key] = (key, key_hash, value)
                return
        if self.size == int(self.capacity * (2 / 3)):
            self._resize()
        index_of_key = self._get_index(key)
        if self.table[index_of_key] is None:
            self.table[index_of_key] = (key, key_hash, value)
            self.size += 1
            return
        if self.table[index_of_key] is not None:
            if key != self.table[index_of_key][0]:
                while self.table[index_of_key] is not None:
                    if key == self.table[index_of_key][0]:
                        self.table[index_of_key] = (key, key_hash, value)
                        return
                    index_of_key = (index_of_key + 1) % self.capacity
                    if self.table[index_of_key] is None:
                        self.table[index_of_key] = (key, key_hash, value)
                        self.size += 1
                        return

    def __getitem__(self, key: Any) -> Any:
        result_index = self._get_index(key)
        if self.table[result_index] is None:
            raise KeyError(f"Key {key} not found")
        if key == self.table[result_index][0]:
            return self.table[result_index][2]
        while (self.table[result_index] is not None and key
               != self.table[result_index][0]):
            result_index = (result_index + 1) % self.capacity
            if self.table[result_index] is not None:
                if key == self.table[result_index][0]:
                    return self.table[result_index][2]
        raise KeyError(f"Key {key} not found")

    def _load_factory(self) -> int | float:
        threshold = self.capacity * (2 / 3)
        return threshold

    def __delitem__(self, key: Any) -> None:
        index_for_delete = self._get_index(key)
        del self.table[index_for_delete]

    def _resize(self) -> None:
        threshold = self._load_factory()
        if int(threshold) == self.size:
            self.capacity *= 2
            old_table = self.table.copy()
            self.table = [None] * self.capacity
            for i in range(len(old_table)):
                if old_table[i] is not None:
                    key = old_table[i][0]
                    key_hash = old_table[i][1]
                    value = old_table[i][2]
                    index_now = key_hash % self.capacity
                    if self.table[index_now] is not None:
                        while self.table[index_now] is not None:
                            index_now = (index_now + 1) % self.capacity
                            if self.table[index_now] is None:
                                self.table[index_now] = (key, key_hash, value)
                                break
                    else:
                        self.table[index_now] = (key, key_hash, value)
            del old_table

    def __len__(self) -> int:
        return self.size
