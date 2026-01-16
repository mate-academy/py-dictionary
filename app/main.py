class Node:
    def __init__(self, key, hash_value, value):
        self.key = key
        self.hash_value = hash_value
        self.value = value


class Dictionary:
    def __init__(self, capacity=10, load_factor=0.7):
        self.capacity = capacity
        self.load_factor = load_factor
        self.size = 0
        self.table = [None] * capacity

    def __getitem__(self, key):
        index = self._get_index(key)
        if self.table[index] is not None:
            return self.table[index].value
        else:
            raise KeyError(f"Key '{key}' not found.")

    def __setitem__(self, key, value):
        index = self._get_index(key)
        hash_value = hash(key)
        node = Node(key, hash_value, value)
        if self.table[index] is None:
            self.table[index] = node
            self.size += 1
            if self.size > self.capacity * self.load_factor:
                self._resize()
        else:
            raise KeyError(f"Key '{key}' already exists.")

    def __len__(self):
        return self.size

    def _get_index(self, key):
        return hash(key) % self.capacity

    def _resize(self):
        self.capacity *= 2
        new_table = [None] * self.capacity
        for node in self.table:
            if node is not None:
                index = node.hash_value % self.capacity
                new_table[index] = node
        self.table = new_table

