class Dictionary:
    def __init__(self) -> None:
        self.capacity = 10
        self.threshold = 0.8
        self.size = 0
        self.table = [[] for _ in range(self.capacity)]

    def __setitem__(self, key: object, value: object) -> None:
        if self.size / self.capacity > self.threshold:
            self.capacity *= 2
            new_table = [[] for _ in range(self.capacity)]
            self.size = 0

            for node in self.table:
                for item in node:
                    new_table[item.hash % self.capacity].append(item)
                    self.size += 1

            self.table = new_table

        node = self.table[hash(key) % self.capacity]

        for i, item in enumerate(node):
            if item.hash != hash(key):
                continue
            if item.key == key:
                node[i] = Item(key, hash(key), value)
                return

        node.append(Item(key, hash(key), value))
        self.size += 1

    def __getitem__(self, key: object) -> object:
        for item in self.table[hash(key) % self.capacity]:
            if item.hash != hash(key):
                continue
            if item.key == key:
                return item.value
        raise KeyError()

    def __len__(self) -> int:
        return self.size


class Item:
    def __init__(self, key: object, key_hash: int, value: object) -> None:
        self.key = key
        self.hash = key_hash
        self.value = value
