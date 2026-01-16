class Node:
    def __init__(self, key: str, value: int) -> None:
        self.key = key
        self.value = value
        self.hash = hash(key)
        self.next = None


class Dictionary:
    def __init__(self, initial_capacity: int = 8) -> None:
        self.capacity = initial_capacity
        self.size = 0
        self.buckets = [None] * self.capacity
        self.load_factor = 0.75

    def __setitem__(self, key: str, value: int) -> None:
        index = self._get_index(key)
        node = self.buckets[index]

        if node is None:
            self.buckets[index] = Node(key, value)
            self.size += 1
        else:
            while node:
                if node.key == key:
                    node.value = value
                    return
                if node.next is None:
                    node.next = Node(key, value)
                    self.size += 1
                    break
                node = node.next

        if self.size / self.capacity > self.load_factor:
            self._resize()

    def __getitem__(self, key: str) -> None:
        index = self._get_index(key)
        node = self.buckets[index]

        while node:
            if node.key == key:
                return node.value
            node = node.next

        raise KeyError(f"Key {key} not found")

    def __len__(self) -> int:
        return self.size

    def _get_index(self, key: str) -> int:
        return hash(key) % self.capacity

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_buckets = [None] * new_capacity

        for i in range(self.capacity):
            node = self.buckets[i]
            while node:
                new_index = node.hash % new_capacity
                if new_buckets[new_index] is None:
                    new_buckets[new_index] = Node(node.key, node.value)
                else:
                    current = new_buckets[new_index]
                    while current.next:
                        current = current.next
                    current.next = Node(node.key, node.value)
                node = node.next

        self.buckets = new_buckets
        self.capacity = new_capacity
