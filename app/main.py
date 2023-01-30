class Dictionary:

    def __init__(self):
        self.capacity = 8
        self.length = 0
        self.dict = [[] for _ in range(self.capacity)]

    def __setitem__(self, key, value):
        hash_ = hash(key)
        index_ = hash_ % self.capacity
        while self.dict[index_]:
            if self.dict[index_][0] == key \
                    and self.dict[index_][2] == hash_:
                self.dict[index_] = [key, value, hash_]
                self.length -= 1
                break
            index_ = (index_ + 1) % self.capacity
        self.dict[index_] = [key, value, hash_]
        self.length += 1
        if self.length == int(self.capacity * (2 / 3)):
            self.resize()

    def __getitem__(self, key):
        hash_ = hash(key)
        index_ = hash_ % self.capacity
        while self.dict[index_]:
            if self.dict[index_][0] == key\
                    and self.dict[index_][2] == hash_:
                return self.dict[index_][1]
            index_ = (index_ + 1) % self.capacity
        raise KeyError

    def resize(self):
        self.capacity *= 2
        all_items = self.dict
        self.dict = [[] for _ in range(self.capacity)]
        self.length = 0
        for item in all_items:
            if item:
                self.__setitem__(item[0], item[1])

    def __len__(self):
        return self.length
