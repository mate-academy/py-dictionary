class Dictionary:
    def __init__(self, capacity: int = 10, load_factor: float = 0.75) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.size = 0
        self.table = [[] for _ in range(self.capacity)]

    def __setitem__(self, key: any, value: any) -> None:
        if self.size / self.capacity > self.load_factor:
            self.resize()
        index = self.hash(key)
        for node in self.table[index]:
            if node[0] == key:
                node[1] = value
                return
        self.table[index].append([key, value])
        self.size += 1

    def __getitem__(self, key: any) -> None:
        index = self.hash(key)
        for node in self.table[index]:
            if node[0] == key:
                return node[1]
        raise KeyError("Key not found: {}".format(key))

    def __len__(self) -> None:
        return self.size

    def __delitem__(self, key: any) -> None:
        index = self.hash(key)
        for i, node in enumerate(self.table[index]):
            if node[0] == key:
                del self.table[index][i]
                self.size -= 1
                return
        raise KeyError("Key not found: {}".format(key))

    def clear(self) -> None:
        self.table = [[] for _ in range(self.capacity)]
        self.size = 0

    def get(self, key: any, default: None = None) -> None:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: any, default: None = None) -> None:
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            return default

    def update(self, other: any) -> None:
        for key, value in other.items():
            self[key] = value

    def __iter__(self) -> None:
        for node_list in self.table:
            for node in node_list:
                yield node[0]

    def resize(self) -> None:
        self.capacity *= 2
        new_table = [[] for _ in range(self.capacity)]
        for node_list in self.table:
            for node in node_list:
                index = self.hash(node[0])
                new_table[index].append(node)
        self.table = new_table

    def hash(self, key: any) -> None:
        return hash(key) % self.capacity
