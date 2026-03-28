class Dictionary:
    def __init__(self):
        self.capacity = 8
        self.size = 0
        self.load_factor = 2 / 3
        self.hash_table = [None for _ in range(self.capacity)]
        self.temporary_cells = []

    def __getitem__(self, key):
        hash_ = hash(key)
        cell = hash_ % self.capacity

        while self.hash_table[cell] is not None:
            if self.hash_table[cell][0] == hash_ and \
                    self.hash_table[cell][1] == key:
                return self.hash_table[cell][2]

            cell = (cell + 1) % self.capacity

        raise KeyError(f"No such key({key})")

    def increase_size_of_hash_table(self):
        self.capacity *= 2
        self.size = 0
        self.temporary_cells = [cell
                                for cell in self.hash_table
                                if cell is not None]
        self.hash_table = [None for _ in range(self.capacity)]
        for cell in self.temporary_cells:
            self.__setitem__(cell[1], cell[2])

    def __setitem__(self, key, value):
        if self.size + 1 > self.capacity * self.load_factor:
            self.increase_size_of_hash_table()

        hash_ = hash(key)
        index_ = hash_ % self.capacity
        cell = [hash_, key, value]

        while self.hash_table[index_] is not None:
            if self.hash_table[index_][0] == hash_ and \
                    self.hash_table[index_][1] == key:
                self.hash_table[index_][2] = value
                return

            index_ = (index_ + 1) % self.capacity

        self.hash_table[index_] = cell
        self.size += 1

    def __len__(self):
        return self.size
