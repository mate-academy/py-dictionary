class Dictionary:

    def __init__(self):
        self.capacity = 8
        self.size = 0
        self.new_dict = [None for i in range(self.capacity)]

    def __setitem__(self, key, value, hash_=None):
        hash_ = hash(key)
        index = hash_ % self.capacity

        while True:
            if not self.new_dict[index]:
                self.new_dict[index] = [hash_, key, value]
                self.size += 1
                break
            if self.new_dict[index][1] == key:
                self.new_dict[index][2] = value
                break
            index = (index + 1) % self.capacity

        if self.size > int(self.capacity * (2 / 3)):
            self.resize()

    def __getitem__(self, item):
        hash_ = hash(item)
        index = hash_ % self.capacity
        while self.new_dict[index] is not None:
            if self.new_dict[index][0] == hash_ and \
                    self.new_dict[index][1] == item:
                return self.new_dict[index][2]
            index = (index + 1) % self.capacity

        raise KeyError(f"new_dict has not {item}")

    def __len__(self):
        return self.size

    def resize(self):
        self.capacity *= 2
        self.size = 0
        old_dict = [element for element in self.new_dict if element]
        self.new_dict = [None for _ in range(self.capacity)]
        for hash_, key, value in old_dict:
            self.__setitem__(key, value, hash_)
