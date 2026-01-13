from typing import Any, List, Optional


class Point:
    def __init__(self, x: Any, y: Any) -> None:
        self.x = x
        self.y = y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y


class Dictionary:
    def __init__(self) -> None:
        self.capacity: int = 8
        self.size: int = 0
        self.table: List[List[List[Any]]] = [[] for _ in range(self.capacity)]
        self.load_factor: float = 0.66

    def __setitem__(self, key: Any, value: Any) -> None:
        key_hash: int = hash(key)
        index: int = key_hash % self.capacity

        for node in self.table[index]:
            if node[0] == key:
                node[1] = value
                return

        self.table[index].append([key, value, key_hash])
        self.size += 1

        if self.size / self.capacity > self.load_factor:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        index: int = hash(key) % self.capacity
        for k, v, h in self.table[index]:
            if k == key:
                return v
        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        old_table: List[List[List[Any]]] = self.table
        self.capacity *= 2
        self.size = 0
        self.table = [[] for _ in range(self.capacity)]

        for bucket in old_table:
            for key, value, key_hash in bucket:
                self._reinsert(key, value, key_hash)

    def _reinsert(self, key: Any, value: Any, key_hash: int) -> None:
        index: int = key_hash % self.capacity
        self.table[index].append([key, value, key_hash])
        self.size += 1

    def __delitem__(self, key: Any) -> None:
        index: int = hash(key) % self.capacity
        bucket: List[List[Any]] = self.table[index]
        for i in range(len(bucket)):
            if bucket[i][0] == key:
                bucket.pop(i)
                self.size -= 1
                return
        raise KeyError(key)

    def clear(self) -> None:
        self.capacity = 8
        self.size = 0
        self.table = [[] for _ in range(self.capacity)]

    def get(self, key: Any, default: Optional[Any] = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default
