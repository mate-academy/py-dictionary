class Dictionary:
    def __init__(self, size: int = 8) -> None:
        self.size = size
        self.table = [None] * self.size
        self.count = 0

    def __setitem__(self, key: any, value: any) -> None:
        if self.count >= (2 * self.size) // 3:
            self.dict_resize()

        index = hash(key) % self.size

        while self.table[index] is not None and self.table[index][0] != key:
            index = (index + 1) % self.size

        if self.table[index] is None:
            self.count += 1

        self.table[index] = (key, value)

    def __getitem__(self, key: any) -> any:
        index = hash(key) % self.size
        initial_index = index

        while self.table[index] is not None:
            if self.table[index][0] == key:
                return self.table[index][1]
            index = (index + 1) % self.size
            if index == initial_index:
                break

        raise KeyError(f"Key '{key}' not found.")

    def __len__(self) -> int:
        return self.count

    def dict_resize(self) -> None:
        old_table = self.table
        self.size *= 2
        self.table = [None] * self.size
        self.count = 0

        for item in old_table:
            if item is not None:
                self[item[0]] = item[1]
