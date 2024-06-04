class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.hash_table = self.create_hash_table()
        self.load_factor = self.calculate_load_factor()
        self.size = 0

    def calculate_load_factor(self) -> int:
        return int(self.capacity * (2 / 3))

    def create_hash_table(self) -> list:
        return [None for _ in range(self.capacity)]

    def __setitem__(self, key: any, value: any) -> None:
        key_hash = hash(key)
        position_in_table = key_hash % self.capacity

        while True:
            if not self.hash_table[position_in_table]:
                self.hash_table[position_in_table] = (key, value, key_hash)
                self.size += 1
                if self.size == self.load_factor:
                    self.increase_capacity()
                break
            elif self.hash_table[position_in_table][0] == key:
                self.hash_table[position_in_table] = (key, value, key_hash)
                break
            position_in_table += 1
            position_in_table %= self.capacity

    def __getitem__(self, item: any) -> any:
        key_hash = hash(item)
        position_in_table = key_hash % self.capacity

        while True:
            if not self.hash_table[position_in_table]:
                raise KeyError
            if self.hash_table[position_in_table][0] == item:
                return self.hash_table[position_in_table][1]
                break
            position_in_table += 1
            position_in_table %= self.capacity

    def increase_capacity(self) -> None:
        self.capacity *= 2
        self.load_factor = self.calculate_load_factor()
        old_hash_table = self.hash_table.copy()
        self.hash_table = self.create_hash_table()
        self.size = 0
        for node in old_hash_table:
            if node:
                key, value, key_hash = node
                self.__setitem__(key, value)

    def __len__(self) -> int:
        return self.size
