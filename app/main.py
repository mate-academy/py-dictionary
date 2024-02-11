class Node:
    def __init__(self, key: int, value: int) -> None:
        self.key = key
        self.value = value
        self.hash = hash(key)


class Dictionary:
    def __init__(self, capacity: int = 10) -> None:
        self.capacity = capacity
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]

    def __hash(self, key: int) -> int:
        return hash(key) % self.capacity

    def __setitem__(self, key: int, value: int) -> None:
        if self.size + 1 > self.capacity // 2:
            self.__resize()
        index = self.__hash(key)
        for node in self.buckets[index]:
            if node.key == key:
                node.value = value
                return
        node = Node(key, value)
        self.buckets[index].append(node)
        self.size += 1

    def __getitem__(self, key: int) -> int:
        index = self.__hash(key)
        for node in self.buckets[index]:
            if node.key == key:
                return node.value
        raise KeyError("Key not found")

    def __len__(self) -> int:
        return self.size

    def __resize(self) -> None:
        self.capacity *= 2
        new_buckets = [[] for _ in range(self.capacity)]
        for bucket in self.buckets:
            for node in bucket:
                new_index = self.__hash(node.key)
                new_buckets[new_index].append(node)
        self.buckets = new_buckets
