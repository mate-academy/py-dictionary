class Dictionary:
    """Najprostsza możliwa implementacja słownika (hash table)."""

    def __init__(self, initial_capacity: int = 4) -> None:
        self.capacity = initial_capacity
        self.size = 0
        self.table = [[] for _ in range(self.capacity)]

    def _cell_index(self, hashed_key: any) -> int:
        # wybieramy numer komórki na podstawie gotowego hasha
        return hashed_key % self.capacity

    def __setitem__(self, key: any, value: any) -> None:
        hashed_key = hash(key)
        index = self._cell_index(hashed_key)
        cell = self.table[index]

        # sprawdzamy, czy klucz już istnieje
        for i, (k, h, v) in enumerate(cell):
            if k == key:
                # nadpisujemy istniejący element
                cell[i] = (key, hashed_key, value)
                return

        # jeśli nie było, dodajemy nowy węzeł (key, hash, value)
        cell.append((key, hashed_key, value))
        self.size += 1

        # jeśli jest za pełno → rozszerz
        if self.size / self.capacity > 0.75:
            self._resize()

    def __getitem__(self, key: any) -> any:
        hashed_key = hash(key)
        index = self._cell_index(hashed_key)
        cell = self.table[index]

        for k, h, v in cell:
            if k == key:
                return v

        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [[] for _ in range(self.capacity)]
        self.size = 0

        # przepisujemy stare elementy do nowej tabeli
        for cell in old_table:
            for key, hashed_key, value in cell:
                self[key] = value
