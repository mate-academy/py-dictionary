class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.hash_table = [None] * self.capacity
        self.load_factor = 2 / 3
        self.length = 0

    def __setitem__(self, key: any, value: any) -> None:
        if self.length == round(self.capacity * self.load_factor):
            self.resize_table()

        index = self.get_index(key)

        if self.hash_table[index] is None:
            self.hash_table[index] = (key, value)
            self.length += 1
        elif self.hash_table[index] is not None:
            self.hash_table[index] = (key, value)

    def __getitem__(self, key: any) -> None:
        index = self.get_index(key)
        if self.hash_table[index] is None:
            raise KeyError
        return self.hash_table[index][1]

    def get_index(self, key: any) -> int:
        index = hash(key) % self.capacity
        while (self.hash_table[index] is not None
               and self.hash_table[index][0] != key):
            index = (index + 1) % self.capacity
        return index

    def __len__(self) -> int:
        return self.length

    def resize_table(self) -> None:
        old_hash_table = self.hash_table.copy()
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.length = 0
        for el in old_hash_table:
            if el:
                self.__setitem__(*el)

    def clear(self) -> None:
        self.__init__()

    def get(self, key: any, value: any = None) -> any:
        try:
            self.__getitem__(key)
        except KeyError:
            return value

    def update(self, iterable_value: dict) -> None:
        for key, value in iterable_value.items():
            self.__setitem__(key, value)
