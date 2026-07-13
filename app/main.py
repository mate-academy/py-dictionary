class Node:
    def __init__(
        self,
        key: object,
        key_hash: int,
        value: object,
    ) -> None:
        self.key = key
        self.hash = key_hash
        self.value = value


class Dictionary:
    initial_capacity = 8
    max_load_factor = 0.7

    def __init__(self) -> None:
        self.length = 0
        self.hash_table: list[Node | None] = [
            None
        ] * self.initial_capacity

    def __len__(self) -> int:
        return self.length

    def __setitem__(self, key: object, value: object) -> None:
        key_hash = hash(key)
        index = self._find_index(key, key_hash)
        node = self.hash_table[index]

        if node is not None:
            node.value = value
            return

        if (self.length + 1) / len(self.hash_table) > self.max_load_factor:
            self._resize()
            index = self._find_index(key, key_hash)

        self.hash_table[index] = Node(key, key_hash, value)
        self.length += 1

    def __getitem__(self, key: object) -> object:
        key_hash = hash(key)
        index = self._find_index(key, key_hash)
        node = self.hash_table[index]

        if node is None:
            raise KeyError(f"Key not found: {key!r}")

        return node.value

    def _find_index(self, key: object, key_hash: int) -> int:
        index = key_hash % len(self.hash_table)

        for _ in range(len(self.hash_table)):
            node = self.hash_table[index]
            if node is None:
                return index
            if node.hash == key_hash and node.key == key:
                return index
            index = (index + 1) % len(self.hash_table)

        raise RuntimeError("Hash table has no available slots")

    def _resize(self) -> None:
        old_table = self.hash_table
        self.hash_table = [None] * (len(old_table) * 2)

        for node in old_table:
            if node is not None:
                index = self._find_index(node.key, node.hash)
                self.hash_table[index] = node
