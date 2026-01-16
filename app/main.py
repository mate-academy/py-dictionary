from typing import Any, Hashable, Optional, List, Tuple, Iterator, Dict


class Dictionary:
    def __init__(
            self,
            initial_capacity: int = 8,
            load_factor: float = 0.75
    ) -> None:
        self.capacity: int = initial_capacity
        self.load_factor: float = load_factor
        self.size: int = 0
        self.table: (
            List[Optional[List[Tuple[int, Hashable, Any]]]]
        ) = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size / self.capacity >= self.load_factor:
            self._resize()
        index = hash(key) % self.capacity
        if self.table[index] is None:
            self.table[index] = []
        for i, (h, k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (hash(key), key, value)
                return
        self.table[index].append((hash(key), key, value))
        self.size += 1

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity
        if self.table[index] is not None:
            for h, k, v in self.table[index]:
                if k == key:
                    return v
        raise KeyError(f"Key {key} not found")

    def __delitem__(self, key: Hashable) -> None:
        index = hash(key) % self.capacity
        if self.table[index] is not None:
            for i, (h, k, v) in enumerate(self.table[index]):
                if k == key:
                    del self.table[index][i]
                    self.size -= 1
                    return

        raise KeyError(f"Key {key} not found")

    def __len__(self) -> int:
        return self.size

    def clear(self) -> None:
        self.table = [None] * self.capacity
        self.size = 0

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
            if default is not None:
                return default
            raise

    def update(self, other: Dict[Hashable, Any]) -> None:
        for key, value in other.items():
            self[key] = value

    def __iter__(self) -> Iterator[Any]:
        for slot in self.table:
            if slot is not None:
                for h, k, v in slot:
                    yield k

    def _resize(self) -> None:
        new_capacity: int = self.capacity * 2
        new_tabl: (
            List[Optional[List[Tuple[int, Any, Any]]]]
        ) = [None] * new_capacity
        for slot in self.table:
            if slot is not None:
                for h, k, v in slot:
                    new_index: int = h % new_capacity
                    if new_tabl[new_index] is None:
                        new_tabl[new_index] = []
                    new_tabl[new_index].append((h, k, v))
        self.table = new_tabl
        self.capacity = new_capacity
