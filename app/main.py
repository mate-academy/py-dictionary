class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.hash_table: list = [None] * 8

    def __len__(self) -> int:
        return self.length

    def __setitem__(self, key, value) -> None:
        hash_key = hash(key)
        index_key = hash_key % len(self.hash_table)
        if self.hash_table[index_key] is None:
            self.hash_table[index_key] = (key, hash_key, value)
        else:
            if self.hash_table[index_key][0] == key:
                self.hash_table[index_key] = (key, hash_key, value)
            else:
                while self.hash_table[index_key] is not None:
                    self.hash_table[index_key + 1] = (key, hash_key, value)

    def __getitem__(self, key):

    