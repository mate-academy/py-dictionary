from typing import Any, Hashable, Iterator


class Dictionary:
    _TOMBSTONE = object()

    class _Node:
        def __init__(self, key: Hashable, hash_value: int, value: Any) -> None:
            self.key = key
            self.hash = hash_value
            self.value = value

    def __init__(self) -> None:
        self.capacity = 8
        self.length = 0
        self.hash_table: list = [None] * self.capacity
        self.load_factor = 0.75

    def _find_slot(self, key: Hashable, key_hash: int) -> int:
        index = key_hash % self.capacity
        first_tombstone = None
        for _ in range(self.capacity):
            node = self.hash_table[index]
            if node is None:
                return (
                    first_tombstone if first_tombstone is not None else index
                )
            if isinstance(node, self._Node):
                if node.key == key:
                    return index
            elif node is self._TOMBSTONE:
                if first_tombstone is None:
                    first_tombstone = index
            index = (index + 1) % self.capacity
        return first_tombstone if first_tombstone is not None else index

    def _resize(self) -> None:
        old_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        for node in old_table:
            if isinstance(node, self._Node):
                index = node.hash % self.capacity
                for _ in range(self.capacity):
                    if self.hash_table[index] is None:
                        self.hash_table[index] = node
                        break
                    index = (index + 1) % self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        key_hash = hash(key)
        index = self._find_slot(key, key_hash)
        slot_content = self.hash_table[index]

        if isinstance(slot_content, self._Node):
            slot_content.value = value
        else:
            self.hash_table[index] = self._Node(key, key_hash, value)
            self.length += 1
            if self.length >= self.capacity * self.load_factor:
                self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        key_hash = hash(key)
        index = self._find_slot(key, key_hash)
        node = self.hash_table[index]
        if isinstance(node, self._Node) and node.key == key:
            return node.value
        raise KeyError(f"Key not found: {key}")

    def __len__(self) -> int:
        return self.length

    def __delitem__(self, key: Hashable) -> None:
        key_hash = hash(key)
        index = self._find_slot(key, key_hash)
        if not isinstance(self.hash_table[index], self._Node):
            raise KeyError(f"Key not found: {key}")
        self.hash_table[index] = self._TOMBSTONE
        self.length -= 1

    def __iter__(self) -> Iterator[Hashable]:
        for node in self.hash_table:
            if isinstance(node, self._Node):
                yield node.key
