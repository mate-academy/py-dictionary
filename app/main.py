from typing import Hashable, Any


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self._size = 0
        self.table = [[] for _ in range(self.capacity)]

    def get_hash(self, key: Any) -> int:
        return hash(key) % self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self._size >= self.capacity * 2 / 3:
            self._resize()

        hash_index = self.get_hash(key)
        slot = self.table[hash_index]

        key_found = False
        index = 0
        while index < len(slot):
            existing_hash, existing_key, existing_value = slot[index]
            if existing_hash == hash_index and existing_key == key:
                slot[index] = (hash_index, key, value)
                key_found = True
                break
            index += 1

        if not key_found:
            slot.append((hash_index, key, value))
            self._size += 1

    def __getitem__(self, key: Any) -> Hashable:
        hash_index = self.get_hash(key)
        slot = self.table[hash_index]

        index = 0
        while index < len(slot):
            existing_hash, existing_key, existing_value = slot[index]
            if existing_hash == hash_index and existing_key == key:
                return existing_value
            index += 1

        raise KeyError(f"Key '{key}' not found")

    def __len__(self) -> int:
        return self._size

    def _resize(self) -> None:
        self.capacity *= 2
        new_table = [[] for _ in range(self.capacity)]

        for bucket in self.table:
            for hash_index, key, value in bucket:
                new_hash_index = hash(key) % self.capacity
                new_table[new_hash_index].append((new_hash_index, key, value))

        self.table = new_table
