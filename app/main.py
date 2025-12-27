class Node:
    def __init__(self, key: any, value: any, key_hash: int) -> None:
        self.key = key
        self.value = value
        self.key_hash = key_hash


class Dictionary:
    def __init__(
            self,
            initial_capacity: int = 8,
            load_factor: float = 0.75
    ) -> None:
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.table = [None] * self.capacity

    def __setitem__(self, key: any, value: any) -> None:
        key_hash = hash(key)
        index = key_hash % self.capacity

        while self.table[index] is not None:
            if self.table[index].key == key:
                self.table[index].value = value
                return
            index = (index + 1) % self.capacity

        self.table[index] = Node(key, value, key_hash)
        self.size += 1

        if self.size / self.capacity >= self.load_factor:
            self._resize()

    def __getitem__(self, key: any) -> any:
        key_hash = hash(key)
        index = key_hash % self.capacity

        while self.table[index] is not None:
            if self.table[index].key == key:
                return self.table[index].value
            index = (index + 1) % self.capacity

        raise KeyError(f"Key '{key}' not found")

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0

        for node in old_table:
            if node is not None:
                self[node.key] = node.value

    def __delitem__(self, key: any) -> None:
        key_hash = hash(key)
        index = key_hash % self.capacity

        while self.table[index] is not None:
            if self.table[index].key == key:
                self.table[index] = None
                self.size -= 1
                self._rehash_after_deletion(index)
                return
            index = (index + 1) % self.capacity

        raise KeyError(f"Key '{key}' not found")

    def _rehash_after_deletion(self, deleted_index: int) -> None:
        current_index = (deleted_index + 1) % self.capacity
        while self.table[current_index] is not None:
            node = self.table[current_index]
            self.table[current_index] = None
            self.size -= 1
            self[node.key] = node.value
            current_index = (current_index + 1) % self.capacity

    def get(self, key: any, default: any = None) -> any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: any, default: any = None) -> any:
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            if default is not None:
                return default
            raise

    def clear(self) -> None:
        self.table = [None] * self.capacity
        self.size = 0

    def update(self, other: dict) -> None:
        for key, value in other.items():
            self[key] = value

    def __iter__(self) -> object:
        for node in self.table:
            if node is not None:
                yield (node.key, node.value)

    def __contains__(self, key: any) -> bool:
        try:
            self[key]
            return True
        except KeyError:
            return False

    def __repr__(self) -> str:
        items = []
        for node in self.table:
            if node is not None:
                items.append(f"{node.key}: {node.value}")
        return "{" + ", ".join(items) + "}"
