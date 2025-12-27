from typing import Any, List, Tuple, Hashable, Iterator


class Dictionary:
    def __init__(self) -> None:
        self.table_size = 8
        self.table: List[List[Tuple[int, Tuple[Hashable, Any]]]] \
            = [[] for _ in range(self.table_size)]
        self.num_elements = 0

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.num_elements >= 2 / 3 * self.table_size:
            self._resize()

        key_hash = self._hash(key)
        bucket = key_hash % self.table_size

        if self.table[bucket] is None:
            self.table[bucket] = [(key_hash, (key, value))]
        else:
            for i, (h, (k, v)) in enumerate(self.table[bucket]):
                if h == key_hash and k == key:
                    self.table[bucket][i] = (key_hash, (key, value))
                    return
            self.table[bucket].append((key_hash, (key, value)))

        self.num_elements += 1

    def __getitem__(self, key: Hashable) -> Any:
        key_hash = self._hash(key)
        bucket = key_hash % self.table_size

        if self.table[bucket] is None:
            raise KeyError(f"Key {key} not found")

        for h, (k, v) in self.table[bucket]:
            if h == key_hash and k == key:
                return v

        raise KeyError(f"Key {key} not found")

    def __delitem__(self, key: Hashable) -> None:
        key_hash = self._hash(key)
        bucket = key_hash % self.table_size

        if self.table[bucket] is None:
            raise KeyError(f"Key {key} not found")

        for i, (h, (k, v)) in enumerate(self.table[bucket]):
            if h == key_hash and k == key:
                del self.table[bucket][i]
                self.num_elements -= 1
                return

        raise KeyError(f"Key {key} not found")

    def _resize(self) -> None:
        old_table = self.table
        self.table_size *= 2
        self.table = [None] * self.table_size
        self.num_elements = 0

        for bucket in old_table:
            if bucket is not None:
                for key_hash, (key, value) in bucket:
                    self.__setitem__(key, value)

    def _hash(self, key: Hashable) -> int:
        if isinstance(key, (list, dict)):
            raise TypeError("Unhashable type: list or dict")
        return hash(key)

    def __len__(self) -> int:
        return self.num_elements

    def __contains__(self, key: Hashable) -> bool:
        key_hash = self._hash(key)
        bucket = key_hash % self.table_size

        if self.table[bucket] is None:
            return False

        return any(h == key_hash and k == key
                   for h, (k, v) in self.table[bucket])

    def items(self) -> List[Tuple[Any, Any]]:
        result = []
        for bucket in self.table:
            if bucket:
                result.extend((k, v) for _, (k, v) in bucket)
        return result

    def keys(self) -> List[Any]:
        return [k for bucket in self.table if bucket for _, (k, v) in bucket]

    def values(self) -> List[Any]:
        return [v for bucket in self.table if bucket for _, (k, v) in bucket]

    def clear(self) -> None:
        self.table = [None] * self.table_size
        self.num_elements = 0

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Hashable, default: Any = None) -> Any:
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            raise

    def update(self, other: dict) -> None:
        for key, value in other.items():
            self[key] = value

    def __iter__(self) -> Iterator:
        return iter(self.keys())
