class Dictionary:

    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = 2 / 3
        self.size = 0
        self.nodes = [None] * self.capacity


    def __setitem__(self, key, value):
        if self.size / self.capacity > self.load_factor:
            self.resize()
        hash_k, index = self.get_hash_and_index(key)

        while self.nodes[index] is not None:
            if self.nodes[index][0] == key:
                self.nodes[index][2] = value
                return
            index = (index + 1) % self.capacity

        self.nodes[index] = [key, hash_k, value]
        self.size += 1

    def __getitem__(self, key):
        _, index = self.get_hash_and_index(key)

        while self.nodes[index] is not None:
            if self.nodes[index][0] == key:
                    return self.nodes[index][2]
            index = (index + 1) % self.capacity
        raise KeyError

    def resize(self):
        old_nodes = self.nodes
        self.capacity *= 2
        self.nodes = [None] * self.capacity
        self.size = 0

        for item in old_nodes:
            if item is not None:
                key = item[0]
                value = item[2]
                self[key] = value

    def get_hash_and_index(self, key):
        hash_k = hash(key)
        index = hash_k % self.capacity
        return hash_k, index

    def __len__(self):
        return self.size
