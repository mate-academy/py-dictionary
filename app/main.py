class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
class Dictionary:
    def __init__(self, initial_capacity=10):
        self.capacity = initial_capacity
        self.size = 0
        self.buckets = [None] * self.capacity

    def __setitem__(self, key, value):
        index = hash(key) % self.capacity
        if self.buckets[index] is None:
            self.buckets[index] = Node(key, value)
        else:
            current = self.buckets[index]
            while current:
                if current.key == key:
                    current.value = value
                    return
                if current.next is None:
                    break
                current = current.next
            current.next = Node(key, value)
        self.size += 1
        if self.size / self.capacity > 0.7:
            self._resize()

    def __getitem__(self, key):
        index = hash(key) % self.capacity
        current = self.buckets[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next
        raise KeyError(f"Key '{key}' not found")

    def __len__(self):
        return self.size

    def _resize(self):
        new_capacity = self.capacity * 2
        new_buckets = [None] * new_capacity
        for i in range(self.capacity):
            current = self.buckets[i]
            while current:
                new_index = hash(current.key) % new_capacity
                if new_buckets[new_index] is None:
                    new_buckets[new_index] = Node(current.key, current.value)
                else:
                    new_current = new_buckets[new_index]
                    while new_current.next:
                        new_current = new_current.next
                    new_current.next = Node(current.key, current.value)
                current = current.next
        self.buckets = new_buckets
        self.capacity = new_capacity
