class Dictionary:

    def __init__(self):
        self.initial_capacity = 8
        self.hash_table = [[] for _ in range(self.initial_capacity)]
        self.length = 0
        self.threshold = int(self.initial_capacity * 2 / 3)

    def __len__(self):
        return self.length

    def __setitem__(self, key, value):
        key_hash = hash(key)
        node_index = key_hash % self.initial_capacity
        while True:
            if len(self.hash_table[node_index]) == 0:
                self.hash_table[node_index] = [key, value, key_hash]
                self.length += 1
                break
            if key == self.hash_table[node_index][0] and \
                    key_hash == self.hash_table[node_index][2]:
                self.hash_table[node_index] = [key, value, key_hash]
                break
            node_index = (node_index + 1) % self.initial_capacity
        if self.__len__() >= self.threshold:
            self.resize()

    def resize(self):
        self.length = 0
        self.initial_capacity *= 2
        self.threshold = int(self.initial_capacity * 2 / 3)
        old_hash_table = self.hash_table
        self.hash_table = [[] for _ in range(self.initial_capacity)]
        for node in old_hash_table:
            if len(node) != 0:
                self.__setitem__(node[0], node[1])

    def __getitem__(self, key):
        node_index = hash(key) % self.initial_capacity
        node = self.hash_table[node_index]
        while True:
            try:
                if key == node[0] and hash(key) == node[2]:
                    return node[1]
            except IndexError:
                raise KeyError(key)
            if node_index % self.initial_capacity == 0:
                break
            node_index = (node_index + 1) % self.initial_capacity
            node = self.hash_table[node_index]
        raise KeyError(key)
