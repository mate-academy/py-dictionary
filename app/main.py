class Node:
    def __init__(self, key: any, key_hash: int, value: any) -> None:
        self.key: any = key
        self.key_hash: int = key_hash
        self.value: any = value


class Dictionary:
    def __init__(self) -> None:
        self.length: int = 0
        self.capacity: int = 8
        self.hash_table: list = [None] * self.capacity
        self.load_factor_threshold: float = 0.7

    def __setitem__(self, key: any, value: any) -> None:
        key_hash: int = hash(key)
        index: int = key_hash % self.capacity

        for i in range(self.capacity):
            probe_index: int = (index + i) % self.capacity
            node = self.hash_table[probe_index]
            if node is None:
                self.hash_table[probe_index] = Node(key, key_hash, value)
                self.length += 1
                break
            elif node.key == key:
                self.hash_table[probe_index].value = value
                break
        else:
            raise Exception("Dictionary is full!")

        if self.length / self.capacity > self.load_factor_threshold:
            self._resize()

    def _resize(self) -> None:
        old_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.length = 0
        for node in old_table:
            if node is not None:
                self[node.key] = node.value

    def __getitem__(self, key: any) -> any:
        key_hash: int = hash(key)
        index: int = key_hash % self.capacity

        for i in range(self.capacity):
            probe_index: int = (index + i) % self.capacity
            node = self.hash_table[probe_index]
            if node is None:
                break
            if node.key == key:
                return node.value
        raise KeyError(key)

    def __len__(self) -> int:
        return self.length
