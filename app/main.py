class Node:
    def __init__(self, key: any, value: any) -> None:
        self.key = key
        self.value = value
        self.next = None


class Dictionary:
    def __init__(self, capacity: int = 10) -> None:
        self.capacity = capacity
        self.size = 0
        self.table = [None] * capacity
        pass

    def _hash(self, key: any) -> any:
        return hash(key) % self.capacity

    def __setitem__(self, key: any, value: any) -> None:
        index = self._hash(key)

        if self.table[index] is None:
            self.table[index] = Node(key, value)
            self.size += 1
        else:
            current = self.table[index]
            while current:
                if current.key == key:
                    current.value = value
                    return
                current = current.next
            new_node = Node(key, value)
            new_node.next = self.table[index]
            self.table[index] = new_node
            self.size += 1

    def __getitem__(self, key: any) -> any:
        index = self._hash(key)
        current = self.table[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next
        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def clear(self) -> None:
        self.table = [None] * self.capacity
        self.size = 0

    def __delitem__(self, key: any) -> None:
        index = self._hash(key)
        previous = None
        current = self.table[index]
        while current:
            if current.key == key:
                if previous:
                    previous.next = current.next
                else:
                    self.table[index] = current.next
                self.size -= 1
                return
            previous = current
            current = current.next
        raise KeyError(key)
