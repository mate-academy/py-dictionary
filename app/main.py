class Dictionary:
    def __init__(self) -> None:
        self._capacity = 8  # початковий розмір
        self.length = 0
        self.hash_table = [[] for _ in range(self._capacity)]

    def _hash(self, key: str) -> int:
        return hash(key) % self._capacity

    def __len__(self) -> int:
        return self.length

    def __setitem__(self, key: str, value: str) -> None:
        index = self._hash(key)
        # Шукаємо ключ у списку
        for i, (sto_key, _, sto_hash) in enumerate(self.hash_table[index]):
            if sto_hash == hash(key) and sto_key == key:
                self.hash_table[index][i] = (key, value, hash(key))
                return
        # Ключа немає — додаємо
        self.hash_table[index].append((key, value, hash(key)))
        self.length += 1

    def __getitem__(self, key: str) -> str:
        index = self._hash(key)
        for stored_key, stored_value, stored_hash in self.hash_table[index]:
            if stored_hash == hash(key) and stored_key == key:
                return stored_value
        raise KeyError(f"Key {key} not found")
