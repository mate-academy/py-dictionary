class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self._capacity = capacity
        self._buckets = [None] * capacity
        self._size = 0
        self._load_factor = 0.6

    def __setitem__(self, key, value):
        index = hash(key) % self._capacity
        # Треба збільшити розмір словника
        if self._size > round(self._capacity * self._load_factor):
            self._resize()
        # Коли ключа немає в словнику
        if self._buckets[index] is None:
            self._buckets[index] = (key, hash(key), value)
        else:
            while self._buckets[index] is not None and self._buckets[index][0] != key:
                index = (index + 1) % self._capacity
            # Коли ключ вже є в словнику
            if self._buckets[index][0] == key:
                self._buckets[index][2] = value
            # Коли ключа немає в словнику але хеш повторюеться і ми шукаємо нову комірку (Коалізія)
            elif self._buckets[index][0] != key and self._buckets[index][1] == hash(key):
                self._buckets[index] = (key, hash(key), value)
            else:
                raise ValueError
        self._size += 1

    def __getitem__(self, key):
        index = hash(key) % self._capacity
        # шукаємо унікальний ключ
        while self._buckets[index] is not None:
            if self._buckets[index][0] == key and self._buckets[index][1] == hash(key):
                return self._buckets[index][2]
            index = (index + 1) % self._capacity
        raise KeyError

    def _resize(self):
        self._capacity *= 2
        last_buckets = self._buckets
        self.clear()
        for bucket in last_buckets:
            if bucket is not None:
                self.__setitem__(bucket[0], bucket[2])
        del last_buckets

    def __len__(self):
        return self._size

    def clear(self):
        self._buckets = [None] * self._capacity
        self._size = 0

    def __delitem__(self, key):
        index = hash(key) % self._capacity

        if self._buckets[index] is None:
            raise KeyError
        for k, h, v in self._buckets[index]:
            if k == key and h == hash(key):
                self._buckets[index] = None
                self._size -= 1
                return
        raise KeyError

    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def pop(self, key, default=None):
        try:
            value = self.__getitem__(key)
            self.__delitem__(key)
            return value
        except KeyError:
            return default

    def update(self, other):
        for key, value in other.items():
            self.__setitem__(key, value)

    def __iter__(self):
        for bucket in self._buckets:
            if bucket is not None:
                key, _, value = bucket
                yield key


dic = Dictionary()
for i in range(10):
    dic[i] = i
#
# # print(len(dic))
# # del dic[5]
# # print(len(dic))
# # print(dic.get(4))
# # print(dic.pop(3))
for e in dic:
    print(e)
