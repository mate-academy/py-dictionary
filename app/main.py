class Dictionary:
    def __init__(self):
        self._capacity = 8  # початковий розмір
        self._size = 0
        self._table = [None] * self._capacity

    def _hash(self, key):
        return hash(key) % self._capacity

    def __len__(self):
        return self._size

    def __setitem__(self, key, value):
        index = self._hash(key)
         # Збережи ключ і значення в комірку
        
        if self._table[index] is None:
            self._size += 1
        
        self._table[index] = (key, value, hash(key))
          
    def __getitem__(self, key):
        index = self._hash(key)
        # 1. Перевір чи комірка порожня
        if self._table[index] is None:
            raise KeyError(key)
            # 2. Розпакуй і порівняй ключі
        stored_key, stored_value, stored_hash = self._table[index]

        if stored_hash == hash(key) and stored_key == key:
            return stored_value
        # 3. Ключ не знайдено
        raise KeyError(key)




d = Dictionary()
d["apple"] = "яблуко"
d["apple"] = "нове яблуко"  # оновлюємо
print(len(d))  # що виведе?
