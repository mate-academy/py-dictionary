class Node:
    def __init__(self, key: any, value: any) -> None:
        self.key = key
        self.hash = hash(key)
        self.value = value
        self.next = None


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.load_factor = 0.75
        self.table = [None] * capacity
        self.size = 0

    def __setitem__(self, key: any, value: any) -> None:
        if self.size / self.capacity >= self.load_factor:
            self._resize()

        index = hash(key) % self.capacity

        if self.table[index] is None:
            self.table[index] = Node(key, value)
            self.size += 1
            return

        current = self.table[index]

        while current:
            if current.key == key:
                current.value = value
                return
            if current.next is None:
                break
            current = current.next

        current.next = Node(key, value)
        self.size += 1

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_table = [None] * new_capacity

        for node in self.table:
            while node:
                new_index = hash(node.key) % new_capacity
                if new_table[new_index] is None:
                    new_table[new_index] = Node(node.key, node.value)
                else:
                    current = new_table[new_index]
                    while current.next:
                        current = current.next
                    current.next = Node(node.key, node.value)
                node = node.next
        self.capacity = new_capacity
        self.table = new_table

    def __getitem__(self, item: any) -> any:
        index = hash(item) % self.capacity
        if self.table[index] is None:
            raise KeyError(f"Key {item}, not found!")
        current = self.table[index]
        while current:
            if current.key == item:
                return current.value
            current = current.next
        raise KeyError(f"Key {item}, not found!")

    def __len__(self) -> int:
        return self.size
