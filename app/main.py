from typing import Any, List, Optional, Tuple, Iterator


class Dictionary:
    def __init__(self) -> None:
        self.capacity: int = 8
        self.size: int = 0
        self.load_factor: float = 2 / 3
        self.table: List[Optional[Tuple[Any, Any, int]]]\
            = [None] * self.capacity

    # Dodawanie / aktualizacja klucza
    def __setitem__(self, key: Any, value: Any) -> None:
        if (self.size / self.capacity) > self.load_factor:
            self._resize()

        h: int = hash(key)
        idx: int = h % self.capacity
        start_idx: int = idx

        while self.table[idx] is not None:
            k, v, kh = self.table[idx]
            if k == key:
                self.table[idx] = (key, value, h)
                return
            idx = (idx + 1) % self.capacity
            if idx == start_idx:
                raise RuntimeError("Tabela pełna, resize się nie powiódł")

        self.table[idx] = (key, value, h)
        self.size += 1

    # Pobieranie wartości
    def __getitem__(self, key: Any) -> Any:
        h: int = hash(key)
        idx: int = h % self.capacity
        start_idx: int = idx

        while self.table[idx] is not None:
            k, v, kh = self.table[idx]
            if k == key:
                return v
            idx = (idx + 1) % self.capacity
            if idx == start_idx:
                break

        raise KeyError(key)

    # Usuwanie klucza
    def __delitem__(self, key: Any) -> None:
        h: int = hash(key)
        idx: int = h % self.capacity
        start_idx: int = idx

        while self.table[idx] is not None:
            k, v, kh = self.table[idx]
            if k == key:
                self.table[idx] = None
                self.size -= 1
                self._rehash_from(idx)
                return
            idx = (idx + 1) % self.capacity
            if idx == start_idx:
                break
        raise KeyError(key)

    # Liczba elementów
    def __len__(self) -> int:
        return self.size

    # Pobieranie wartości z domyślną
    def get(self, key: Any, default: Optional[Any] = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    # Usuwanie i zwracanie wartości
    def pop(self, key: Any, default: Optional[Any] = None) -> Any:
        try:
            value: Any = self[key]
            del self[key]
            return value
        except KeyError:
            if default is not None:
                return default
            else:
                raise

    # Czyszczenie słownika (O(n), zachowuje pojemność)
    def clear(self) -> None:
        self.size = 0
        for i in range(self.capacity):
            self.table[i] = None

    # Aktualizacja z innego słownika
    def update(self, other: "Dictionary") -> None:
        for k, v in other.items():
            self[k] = v

    # Iterator po kluczach
    def __iter__(self) -> Iterator[Any]:
        for entry in self.table:
            if entry is not None:
                k, v, h = entry
                yield k

    # Podwajanie pojemności
    def _resize(self) -> None:
        old_table: List[Optional[Tuple[Any, Any, int]]] = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0

        for entry in old_table:
            if entry is not None:
                k, v, h = entry
                self[k] = v

    # Rehash dla usuwania elementów
    def _rehash_from(self, empty_idx: int) -> None:
        idx: int = (empty_idx + 1) % self.capacity
        while self.table[idx] is not None:
            k, v, h = self.table[idx]
            self.table[idx] = None
            self.size -= 1
            self[k] = v
            idx = (idx + 1) % self.capacity

    # Zamiana na listę tuple (do testów)
    def items(self) -> List[Tuple[Any, Any]]:
        return [(k, v) for entry in self.table
                if entry is not None for k, v, h in [entry]]
