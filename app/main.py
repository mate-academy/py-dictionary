class Dictionary:
    def __init__(self):
        self.capacity = 0
        self.dict_length = 8
        self.my_dict = [None for _ in range(self.dict_length)]

    def __setitem__(self, key, value, hash_=None):
        if hash_ is None:
            hash_ = hash(key)
        index = hash_ % self.dict_length
        while True:
            if not self.my_dict[index]:
                self.my_dict[index] = [hash_, key, value]
                self.capacity += 1
                break
            if self.my_dict[index][1] == key:
                self.my_dict[index][2] = value
                break
            index = (index + 1) % self.dict_length
        if self.capacity > int(self.dict_length * 2 / 3):
            self.resize()

    def __getitem__(self, key):
        hash_ = hash(key)
        index = hash_ % self.dict_length
        for _ in range(self.dict_length):
            if self.my_dict[index][1] == key:
                return self.my_dict[index][2]
            index = (index + 1) % self.dict_length
        else:
            raise KeyError(f"Key: {key} not in dictionary!")

    def __len__(self):
        return self.capacity

    def resize(self):
        self.capacity = 0
        self.dict_length *= 2
        old_dict = [item for item in self.my_dict if item]
        self.my_dict = [None for _ in range(self.dict_length)]
        for hash_, key, value in old_dict:
            self.__setitem__(key, value, hash_)

    def clear(self):
        self.capacity = 0
        self.my_dict = [None for _ in range(self.dict_length)]

    def __delitem__(self, key):
        hash_ = hash(key)
        index = hash_ % self.dict_length
        for _ in range(self.dict_length):
            if self.my_dict[index][1] == key:
                self.my_dict[index] = None
                self.capacity -= 1
                break
            index = (index + 1) % self.dict_length
        else:
            raise KeyError(f"Key: {key} not in dictionary!")
