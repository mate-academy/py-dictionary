from typing import Any, Optional


class _Deleted:
    def __repr__(self) -> str:
        return "<DELETED>"


DELETED = _Deleted()


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.value = value
        self.hash = hash(self.key)


class Dictionary:
    def __init__(self) -> None:
        self.capacity: int = 8
        self.hash_table: list[
            Optional[Node | _Deleted]
        ] = [None] * self.capacity
        self.length: int = 0

    def __setitem__(self, key: Any, value: Any) -> None:
        if (self.length + 1) / self.capacity > 2 / 3:
            self._resize()

        idx = hash(key) % self.capacity

        while self.hash_table[idx] is not None:
            node = self.hash_table[idx]
            if node is not DELETED and node.key == key:
                node.value = value
                return
            if node is DELETED:
                break
            idx = (idx + 1) % self.capacity

        self.hash_table[idx] = Node(key, value)
        self.length += 1

    def __getitem__(self, key: Any) -> Any:
        idx = hash(key) % self.capacity
        start_idx = idx

        while self.hash_table[idx] is not None:
            node = self.hash_table[idx]
            if node is not DELETED and node.key == key:
                return node.value
            idx = (idx + 1) % self.capacity
            if idx == start_idx:
                break

        raise KeyError(f"Key {key} not found")

    def __delitem__(self, key: Any) -> None:
        idx = hash(key) % self.capacity
        start_idx = idx

        while self.hash_table[idx] is not None:
            node = self.hash_table[idx]
            if node is not DELETED and node.key == key:
                self.hash_table[idx] = DELETED
                self.length -= 1
                return
            idx = (idx + 1) % self.capacity
            if idx == start_idx:
                break

        raise KeyError(f"Key {key} not found")

    def __len__(self) -> int:
        return self.length

    def _resize(self) -> None:
        old_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.length = 0

        for item in old_table:
            if isinstance(item, Node):
                self.__setitem__(item.key, item.value)
