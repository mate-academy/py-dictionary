class Dictionary:

    def __init__(self):
        self.length = 0
        self.capacity = 8
        self.hash = [None] * self.capacity

    def __len__(self):
        return self.length

    def __getitem__(self, key):
        get_hash_key = hash(key)
        get_index = get_hash_key % self.capacity
        while self.hash[get_index]:
            if self.hash[get_index][1] == get_hash_key and\
                    self.hash[get_index][0] == key:
                return self.hash[get_index][2]
            get_index = (get_index + 1) % self.capacity
        raise KeyError

    def another_size(self):
        self.capacity *= 2
        self.length = 0
        old_hash = self.hash
        self.hash = [None] * self.capacity
        for element in old_hash:
            if element:
                self.__setitem__(element[0], element[2])

    def __setitem__(self, key, value):
        if self.length >= (self.capacity * 2 / 3):
            self.another_size()

        get_hash_key = hash(key)
        get_index = get_hash_key % self.capacity
        while True:
            if not self.hash[get_index]:
                self.hash[get_index] = [key, get_hash_key, value]
                self.length += 1
                break
            if self.hash[get_index][0] == key and\
                    self.hash[get_index][1] == get_hash_key:
                self.hash[get_index][2] = value
                break
            get_index = (get_index + 1) % self.capacity
