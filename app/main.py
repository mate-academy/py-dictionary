class Dictionary:
    def __init__(self, capacity: int = 8, load_factor: float = 2 / 3) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.size = 0
        self.table = [None] * self.capacity

    def __setitem__(self, key: int, value: int) -> None:
        if self.size >= self.capacity * self.load_factor:
            self.resize()
        hash_key = hash(key)
        index = hash_key % self.capacity
        node = self.table[index]
        while node:
            if node[0] == key:
                node[2] = value
                return
            node = node[1]
        self.table[index] = [key, self.table[index], value]
        self.size += 1

    def __getitem__(self, key: int) -> None:
        hash_key = hash(key)
        index = hash_key % self.capacity
        node = self.table[index]
        while node:
            if node[0] == key:
                return node[2]
            node = node[1]
        raise KeyError(key)

    def resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0
        for node in old_table:
            while node:
                self[node[0]] = node[2]
                node = node[1]

    def __len__(self) -> int:
        return self.size
