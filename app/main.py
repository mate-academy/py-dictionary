INITIAL_CAPACITY = 8
RESIZE_STRATEGY = 2


class Dictionary:
    def __init__(
            self
    ) -> None:
        self.length = 0
        self.hash_table = [[] for _ in range(INITIAL_CAPACITY)]

    def __len__(self) -> int:
        return self.length

    def resize(self) -> None:
        old_table = self.hash_table
        self.hash_table = [
            [] for _ in range(len(self.hash_table) * RESIZE_STRATEGY)
        ]
        self.length = 0
        for node_list in old_table:
            for node in node_list:
                self.__setitem__(node[0], node[2])

    def __setitem__(self, key: any, value: any) -> None:
        if self.length >= len(self.hash_table) * 2 / 3:
            self.resize()
        hash_item = hash(key)
        node_index = hash_item % len(self.hash_table)
        if self.hash_table[node_index] == []:
            self.hash_table[node_index].append([key, hash_item, value])
        else:
            for node in self.hash_table[node_index]:
                if key == node[0]:
                    node[2] = value
                    return
            self.hash_table[node_index].append([key, hash_item, value])
        self.length += 1

    def __getitem__(self, key: any) -> any:
        hash_item = hash(key)
        node_index = hash_item % len(self.hash_table)
        if self.hash_table[node_index] == []:
            raise KeyError
        for node in self.hash_table[node_index]:
            if node[0] == key:
                return node[2]
        raise KeyError
