class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.table = [None] * self.capacity
        self.size = 0

    def hash_function(self, key: int) -> None:
        hash_value = hash(key)
        index_in_node = hash_value % self.capacity
        return index_in_node

    def __setitem__(self, key: int, value: int) -> None:
        index = self.hash_function(key)

        if self.table[index] is None:
            self.table[index] = []
        for node in self.table[index]:
            if node[0] == key:
                node[1] = value
                return

        self.table[index].append([key, value])
        self.size += 1

        if self.size / self.capacity > 0.75:
            self.resize()

    def __getitem__(self, key: int) -> None:
        index = self.hash_function(key)

        if self.table[index] is None:
            raise KeyError("Key is not found")
        for node in self.table[index]:
            if node[0] == key:
                return node[1]

        raise KeyError("Key is not found")

    def __len__(self) -> None:
        return self.size

    def resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0

        for chain in old_table:
            if chain is not None:
                for key, value in chain:
                    self.__setitem__(key, value)
