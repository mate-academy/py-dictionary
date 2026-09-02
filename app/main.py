

class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.hash_table = [None] * self.capacity
        self.length = 0

    def __setitem__(self, key: str, value: str) -> None:
        key_hash = hash(key)
        for item in self.hash_table:
            if item is not None and item.key == key:
                item.value = value
                return
        item = Item(key, key_hash, value)
        self.length += 1
        load_factor = self.length / self.capacity
        if load_factor >= 0.75:
            old_table = self.hash_table
            self.capacity *= 2
            self.hash_table = [None] * self.capacity
            for old_item in old_table:
                if old_item is None:
                    continue
                hash_index = old_item.key_hash % self.capacity
                while self.hash_table[hash_index] is not None:
                    hash_index = (hash_index + 1) % self.capacity
                self.hash_table[hash_index] = old_item

        hash_index = key_hash % self.capacity
        while self.hash_table[hash_index] is not None:
            hash_index = (hash_index + 1) % self.capacity
        self.hash_table[hash_index] = item

    def __getitem__(self, key: str) -> str:
        for item in self.hash_table:
            if item is not None and item.key == key:
                return item.value
        raise KeyError(f"{key} not in Dict")

    def __len__(self) -> int:
        return self.length


class Item:
    def __init__(self, key: str, key_hash: int, value: str) -> None:
        self.key = key
        self.key_hash = key_hash
        self.value = value
