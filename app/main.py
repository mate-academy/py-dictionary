from typing import Any


class Dictionary:
    DELETED = object()

    def __init__(self) -> None:
        self._size = 0
        self._capacity = 8
        self._load_factor = 0.66
        self._threshold = self._calc_threshold()
        self._hash_table: list[Any] = [None] * self._capacity

    def _calc_threshold(self) -> int:
        return int(self._capacity * self._load_factor)

    def calc_index(self, key_hash: int) -> int:
        return key_hash % self._capacity

    def clear(self) -> None:
        self._hash_table = [None] * self._capacity
        self._size = 0

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Any, default: Any = DELETED) -> Any:
        key_hash = hash(key)
        index = self.calc_index(key_hash)

        for _ in range(self._capacity):
            slot = self._hash_table[index]
            if slot is None:
                break

            if (
                    slot is not Dictionary.DELETED
                    and slot[0] == key_hash
                    and slot[1] == key
            ):
                value = slot[2]
                self._hash_table[index] = Dictionary.DELETED
                self._size -= 1
                return value

            index = (index + 1) % self._capacity

        if default is not Dictionary.DELETED:
            return default

        raise KeyError(key)

    def _find_slot(self, key_hash: int, key: Any) -> int:
        index = self.calc_index(key_hash)
        first_deleted = None

        for _ in range(self._capacity):
            slot = self._hash_table[index]
            if slot is None:
                if first_deleted is not None:
                    return first_deleted
                return index

            if slot is Dictionary.DELETED:
                if first_deleted is None:
                    first_deleted = index
            elif slot[0] == key_hash and slot[1] == key:
                return index

            index = (index + 1) % self._capacity

        if first_deleted is not None:
            return first_deleted

        raise RuntimeError("Hash table is full")

    def __setitem__(self, key: Any, value: Any) -> None:
        if self._size >= self._threshold:
            self._resize()

        key_hash = hash(key)
        index = self._find_slot(key_hash, key)
        slot = self._hash_table[index]

        if slot is None or slot is Dictionary.DELETED:
            self._hash_table[index] = (key_hash, key, value)
            self._size += 1
            return

        self._hash_table[index] = (key_hash, key, value)

    def _resize(self) -> None:
        old_table = self._hash_table

        self._capacity *= 2
        self._threshold = self._calc_threshold()
        self._hash_table = [None] * self._capacity
        self._size = 0

        for slot in old_table:
            if slot is not None and slot is not Dictionary.DELETED:
                self[slot[1]] = slot[2]

    def __getitem__(self, key: Any) -> Any:
        key_hash = hash(key)
        index = self.calc_index(key_hash)

        for _ in range(self._capacity):
            slot = self._hash_table[index]
            if slot is None:
                break

            if slot is not Dictionary.DELETED:
                if slot[0] == key_hash and slot[1] == key:
                    return slot[2]

            index = (index + 1) % self._capacity

        raise KeyError(key)

    def __len__(self) -> int:
        return self._size

    def __delitem__(self, key: Any) -> None:
        key_hash = hash(key)
        index = self.calc_index(key_hash)

        for _ in range(self._capacity):
            slot = self._hash_table[index]
            if slot is None:
                break

            if slot is not Dictionary.DELETED:
                if slot[0] == key_hash and slot[1] == key:
                    self._hash_table[index] = Dictionary.DELETED
                    self._size -= 1
                    return

            index = (index + 1) % self._capacity

        raise KeyError(key)
