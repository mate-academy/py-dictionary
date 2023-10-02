class Dictionary:

    def __init__(self):
        self.storage = [[] for _ in range(8)]
        self.capacity = 8
        self.length = 0

    def __setitem__(self, key, value):
        if self.length >= 2 / 3 * self.capacity:
            self.resize()
        hash_ = hash(key)
        index = hash_ % self.capacity
        while self.storage[index]:
            if self.storage[index][0] == key \
                    and self.storage[index][1] == hash_:
                self.storage[index][2] = value
                return
            index = (index + 1) % self.capacity
        self.storage[index] = [key, hash_, value]
        self.length += 1

    def __len__(self):
        return self.length

    def resize(self):
        existing_elements = self.storage.copy()
        self.storage = [[] for _ in range(self.capacity * 2)]
        self.capacity *= 2
        self.length = 0
        for element in existing_elements:
            if element:
                self.__setitem__(element[0], element[2])

    def __getitem__(self, key):
        hash_ = hash(key)
        index = hash_ % self.capacity
        while self.storage[index]:
            if self.storage[index][0] == key \
                    and self.storage[index][1] == hash_:
                return self.storage[index][2]
            index = (index + 1) % self.capacity
        raise KeyError
