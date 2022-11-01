class Dictionary:
    def __init__(self):
        self.capacity = 8
        self.length = 0
        self.hash_list = [None for _ in range(self.capacity)]

    def __setitem__(self, key, value, hash_=None):
        if hash_ is None:
            hash_ = hash(key)
        index_ = hash_ % self.capacity
        while True:
            if not self.hash_list[index_]:
                self.hash_list[index_] = [hash_, key, value]
                self.length += 1
                break
            if self.hash_list[index_][1] == key:
                self.hash_list[index_][2] = value
                break
            index_ = (index_ + 1) % self.capacity
        if self.length > int(self.capacity * 2 / 3):
            self.resize()

    def __getitem__(self, key):
        hash_ = hash(key)
        index_ = hash_ % self.capacity
        for _ in range(self.capacity):
            if self.hash_list[index_][1] == key:
                return self.hash_list[index_][2]
            index_ = (index_ + 1) % self.capacity
        else:
            raise KeyError(f"Key: {key} is not in dictionary!")

    def __len__(self):
        return self.length

    def resize(self):
        self.capacity *= 2
        self.length = 0
        old_list = [item for item in self.hash_list if item]
        self.hash_list = [None for _ in range(self.capacity)]
        for hash_, key, value in old_list:
            self.__setitem__(key, value, hash_)

    def clear(self):
        self.capacity = 0
        self.hash_list = [None for _ in range(self.capacity)]

    def __delitem__(self, key):
        hash_ = hash(key)
        index_ = hash_ % self.capacity
        for _ in range(self.capacity):
            if self.hash_list[index_][1] == key:
                self.hash_list[index_] = None
                self.capacity -= 1
                break
            index_ = (index_ + 1) % self.capacity
        else:
            raise KeyError(f"Key: {key} is not in dictionary!")
