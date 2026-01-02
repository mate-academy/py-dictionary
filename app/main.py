from typing import Any, Hashable


class Dictionary:

    LOAD_FACTOR = 0.75

    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.table = [[] for _ in range(capacity)]
        self.size = 0

    def __setitem__(self, key: Hashable, value: Any) -> None:
        incoming_hash = hash(key)
        index = incoming_hash % self.capacity
        bucket = self.table[index]

        for (position,
             (stored_key, stored_value, stored_hash)) in enumerate(bucket):
            if stored_hash == incoming_hash and stored_key == key:
                bucket[position] = (key, value, stored_hash)
                return

        bucket.append((key, value, incoming_hash))
        self.size += 1

        if self.size / self.capacity > self.LOAD_FACTOR:
            self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        incoming_hash = hash(key)
        index = incoming_hash % self.capacity
        bucket = self.table[index]

        for stored_key, stored_value, stored_hash in bucket:
            if stored_hash == incoming_hash and stored_key == key:
                return stored_value

        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [[] for _ in range(self.capacity)]
        self.size = 0

        for bucket in old_table:
            for stored_key, stored_value, _ in bucket:
                self[stored_key] = stored_value
