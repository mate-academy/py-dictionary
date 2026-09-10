from typing import Any, List, Optional


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"


class Dictionary:
    _TOMBSTONE = "DELETED"

    def __init__(self, capacity: int = 8, load_factor: float = 0.66) -> None:
        self.capacity: int = capacity
        self.load_factor: float = load_factor
        self.length: int = 0
        self.hash_table: List[Optional[Any]] = [None] * self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        h = hash(key)
        idx = h % self.capacity
        first_deleted_idx = None

        attempts = 0
        while attempts < self.capacity:
            node = self.hash_table[idx]
            if node is None:
                insert_idx = (
                    first_deleted_idx
                    if first_deleted_idx is not None
                    else idx
                )
                self.hash_table[insert_idx] = (h, key, value)
                self.length += 1
                if self.length / self.capacity > self.load_factor:
                    self._resize()
                return

            if node == Dictionary._TOMBSTONE:
                if first_deleted_idx is None:
                    first_deleted_idx = idx
            else:
                node_hash, node_key, _ = node
                if node_hash == h and node_key == key:
                    self.hash_table[idx] = (h, key, value)
                    return

            idx = (idx + 1) % self.capacity
            attempts += 1

        if first_deleted_idx is not None:
            self.hash_table[first_deleted_idx] = (h, key, value)
            self.length += 1
            if self.length / self.capacity > self.load_factor:
                self._resize()

    def __getitem__(self, key: Any) -> Any:
        h = hash(key)
        idx = h % self.capacity
        attempts = 0
        while attempts < self.capacity:
            node = self.hash_table[idx]
            if node is None:
                raise KeyError(key)

            if node != Dictionary._TOMBSTONE:
                node_hash, node_key, node_val = node
                if node_hash == h and node_key == key:
                    return node_val

            idx = (idx + 1) % self.capacity
            attempts += 1

        raise KeyError(key)

    def __delitem__(self, key: Any) -> None:
        h = hash(key)
        idx = h % self.capacity
        attempts = 0
        while attempts < self.capacity:
            node = self.hash_table[idx]
            if node is None:
                raise KeyError(key)

            if node != Dictionary._TOMBSTONE:
                node_hash, node_key, _ = node
                if node_hash == h and node_key == key:
                    self.hash_table[idx] = Dictionary._TOMBSTONE
                    self.length -= 1
                    return

            idx = (idx + 1) % self.capacity
            attempts += 1

        raise KeyError(key)

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def __contains__(self, key: Any) -> bool:
        try:
            _ = self[key]
            return True
        except KeyError:
            return False

    def __len__(self) -> int:
        return self.length

    def __repr__(self) -> str:
        items = [
            f"{node[1]}: {node[2]}"
            for node in self.hash_table
            if node is not None and node != Dictionary._TOMBSTONE
        ]
        return f"Dictionary({{{', '.join(items)}}})"

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_hash_table: List[Optional[Any]] = [None] * new_capacity
        for node in self.hash_table:
            if node is None or node == Dictionary._TOMBSTONE:
                continue
            h, key, value = node
            idx = h % new_capacity
            while new_hash_table[idx] is not None:
                idx = (idx + 1) % new_capacity
            new_hash_table[idx] = (h, key, value)
        self.capacity = new_capacity
        self.hash_table = new_hash_table
