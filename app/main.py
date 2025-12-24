class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.nodes = [[] for _ in range(8)]
        self.length = 0

    def resize(self) -> None:
        self.capacity *= 2
        old_nodes = self.nodes
        self.nodes = [[] for _ in range(self.capacity)]
        self.length = 0

        for node in old_nodes:
            if node:
                self.__setitem__(node[0], node[1])

    def __setitem__(self, key: any, value: any) -> None:
        bucket = self.nodes[hash(key) % self.capacity]
        for node in bucket:
            if node[0] == key:
                node[1] = value
                return

        bucket.append([key, value, hash(key)])
        self.length += 1

    def __getitem__(self, key: any) -> any:
        bucket = self.nodes[hash(key) % self.capacity]
        for node in bucket:
            if node[0] == key:
                return node[1]
        raise KeyError("There is no such key in the dictionary")

    def __len__(self) -> int:
        return self.length

    def __delitem__(self, key: any) -> None:
        bucket = self.nodes[hash(key) % self.capacity]
        for node in bucket:
            if node[0] == key:
                node[1] = []
                self.length -= 1

    def clear(self) -> None:
        self.__init__()

    def get(self, key: any) -> None:
        try:
            return self.__getitem__(key)
        except KeyError:
            return None

    def pop(self, key: any) -> any:
        result = self.__getitem__(key)
        self.__delitem__(key)
        return result
