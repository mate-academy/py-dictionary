from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.count = 0
        self.dict_size = 8
        self.hash_table = [None] * self.dict_size
        self.load_factor = 0.75

    def resize_dict(self) -> None:
        if self.count / self.dict_size >= self.load_factor:
            new_size = self.dict_size * 2
            new_hash_table = [None] * new_size
            for node in self.hash_table:
                if node:
                    new_index = node[1] % new_size
                    if new_hash_table[new_index] is None:
                        new_hash_table[new_index] = node
                    else:
                        while new_hash_table[new_index] is not None:
                            new_index = (new_index + 1) % new_size
                        new_hash_table[new_index] = node
            self.hash_table = new_hash_table
            self.dict_size = new_size

    def __len__(self) -> int:
        return self.count

    def __getitem__(self, key: Hashable) -> Any:
        get_hash = hash(key)
        idx = get_hash % self.dict_size
        start = idx
        while True:
            slot = self.hash_table[idx]
            if slot is None:
                raise KeyError(key)
            if slot[0] == key:
                return slot[2]
            idx = (idx + 1) % self.dict_size
            if idx == start:
                raise KeyError(key)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        self.resize_dict()
        hash_key = hash(key)
        idx = hash_key % self.dict_size
        node = (key, hash_key, value)
        if self.hash_table[idx] is None:
            self.hash_table[idx] = node
            self.count += 1
            return
        else:
            start = idx
            while True:
                slot = self.hash_table[idx]
                if slot is None:
                    self.hash_table[idx] = node
                    self.count += 1
                    return
                elif slot[0] == key:
                    self.hash_table[idx] = node
                    return
                idx = (idx + 1) % self.dict_size
                if idx == start:
                    raise KeyError(key)
