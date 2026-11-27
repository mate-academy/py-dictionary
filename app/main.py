from typing import Any, Iterable

missing = object()


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.hash = hash(key)
        self.value = value


class Dictionary:
    def __init__(self) -> None:
        self.table: list[Any] = [None] * 8
        self.size = 0
        self.tombstone_size = 0
        self.tombstone = object()

    def __setitem__(self, key: Any, value: Any) -> None:
        pair = Node(key, value)
        first_tombstone = None
        slot_name = pair.hash % len(self.table)
        while True:
            current = self.table[slot_name]
            if current is self.tombstone:
                if first_tombstone is None:
                    first_tombstone = slot_name
            elif current is None:
                insert_slot = first_tombstone\
                    if first_tombstone is not None else slot_name
                if first_tombstone is None:
                    if (((self.size + 1) + self.tombstone_size)
                            / len(self.table) > 2 / 3):
                        self._resize()
                        slot_name = pair.hash % len(self.table)
                        first_tombstone = None
                        continue
                    self.table[slot_name] = pair
                    self.size += 1
                    break
                self.table[insert_slot] = pair
                self.tombstone_size -= 1
                self.size += 1
                break
            elif current.hash == pair.hash and current.key == key:
                self.table[slot_name] = pair
                break
            slot_name = (slot_name + 1) % len(self.table)

    def _resize(self) -> list:
        old_table = self.table
        new_capacity = len(old_table) * 2
        self.table = [None] * new_capacity
        for node in old_table:
            if node is self.tombstone:
                node = None
            if node is None:
                continue
            slot = node.hash % new_capacity
            while self.table[slot] is not None:
                slot = (slot + 1) % new_capacity
            self.table[slot] = node
        self.tombstone_size = 0
        return self.table

    def __getitem__(self, key: Any) -> Any:
        _hash = hash(key)
        slot = _hash % len(self.table)
        while True:
            current = self.table[slot]
            if current is None:
                raise KeyError
            if current.key == key and current.hash == _hash:
                return current.value
            slot = (slot + 1) % len(self.table)

    def __len__(self) -> int:
        return self.size

    def clear(self) -> None:
        self.table = [None] * 8
        self.size = 0

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def update(self, our_items: Iterable[tuple]) -> None:
        for key, value in our_items:
            self[key] = value

    def __delitem__(self, key: Any) -> None:
        _hash = hash(key)
        slot = _hash % len(self.table)
        while True:
            current = self.table[slot]
            if current is None:
                raise KeyError(key)
            if current is not self.tombstone:
                if current.key == key and current.hash == _hash:
                    self.table[slot] = self.tombstone
                    self.size -= 1
                    self.tombstone_size += 1
                    return
            slot = (slot + 1) % len(self.table)

    def pop(self, key: Any, default: Any = missing) -> Any:
        try:
            value = self[key]
        except KeyError:
            if default is missing:
                raise
            return default
        del self[key]
        return value

    def __iter__(self) -> Iterable[Any]:
        for node in self.table:
            if node is not self.tombstone and node is not None:
                yield node.key
