class Dictionary:
    def __init__(self) -> None:
        self._capacity = 8  # початковий розмір
        self._size = 0
        self._table = [[] for _ in range(self._capacity)]

    def _hash(self, key: str) -> int:
        return hash(key) % self._capacity

    def __len__(self) -> int:
        return self._size

    def __setitem__(self, key: str, value: str) -> None:
        index = self._hash(key)
        # Шукаємо ключ у списку
        for i, (stored_key, _, stored_hash) in enumerate(self._table[index]):
            if stored_hash == hash(key) and stored_key == key:
                self._table[index][i] = (key, value, hash(key))
                return
        # Ключа немає — додаємо
        self._table[index].append((key, value, hash(key)))
        self._size += 1

    def __getitem__(self, key: str) -> str:
        index = self._hash(key)
        for stored_key, stored_value, stored_hash in self._table[index]:
            if stored_hash == hash(key) and stored_key == key:
                return stored_value
        raise KeyError(key)
