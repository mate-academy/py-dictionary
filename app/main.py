class Node:
    def __init__(self, key, value):
        self.key = key
        self.hash = hash(key)
        self.value = value

class Dictionary:
    def __init__(self, capacity=8, load_factor=0.7):
        self.capacity = capacity
        self.load_factor = load_factor
        self.size = 0
        self.table = [None] * capacity

    def __setitem__(self, key, value):
        if self.size / self.capacity > self.load_factor:
            self._resize()
        self._insert(key, value)
    
    def _insert(self, key, value):
        index = hash(key) % self.capacity
        while self.table[index] is not None:
            if self.table[index].key == key:
                self.table[index].value = value
                return
            index = (index + 1) % self.capacity
        self.table[index] = Node(key, value)
        self.size += 1

    def __getitem__(self, key):
        index = hash(key) % self.capacity
        while self.table[index] is not None:
            if self.table[index].key == key:
                return self.table[index].value
            index = (index + 1) % self.capacity
        raise KeyError(f'Key {key} not found')

    def __len__(self):
        return self.size

    def _resize(self):
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0
        for node in old_table:
            if node is not None:
                self._insert(node.key, node.value)
