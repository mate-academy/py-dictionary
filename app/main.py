class Dictionary:
    def __init__(
            self, initial_capacity: int = 8,
            load_factor: float = 2 / 3
    ) -> None:
        self.initial_capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.capacity = initial_capacity
        self.table = [None] * initial_capacity

    def __setitem__(self, key: int, value: int) -> None:
        if self.size >= self.capacity * self.load_factor:
            self.resize()

        if self.table[self._get_index(key)] is None:
            self.table[self._get_index(key)] = []

        for entry in self.table[self._get_index(key)]:
            if entry[0] == key:
                entry[2] = value
                return

        self.table[self._get_index(key)].append([key, self._hash(key), value])
        self.size += 1

    def __getitem__(self, key: int) -> None:
        if self.table[self._get_index(key)] is not None:
            for entry in self.table[self._get_index(key)]:
                if entry[0] == key:
                    return entry[2]
        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def _hash(self, key: int) -> int:
        return hash(key)

    def _get_index(self, key: int) -> int:
        return self._hash(key) % self.capacity

    def resize(self) -> None:
        new_capacity = self.capacity * 2
        new_table = [None] * new_capacity

        for entry_list in self.table:
            if entry_list is not None:
                for entry in entry_list:
                    key, _, value = entry
                    new_index = self._hash(key) % new_capacity
                    if new_table[new_index] is None:
                        new_table[new_index] = []
                    new_table[new_index].append([key, self._hash(key), value])

        self.table = new_table
        self.capacity = new_capacity
