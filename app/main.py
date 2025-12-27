class Dictionary:
    def __init__(self):
        self.length_hash = 8
        self.length_dict = 0
        self.capacity = [[] for _ in range(self.length_hash)]

    def __setitem__(self, key, value):
        if self.length_dict >= self.length_hash * 2 // 3:
            self.__resize_hash()
        hash_ = hash(key)
        new_index = hash_ % self.length_hash
        hash_value = new_index
        while True:
            if self.capacity[new_index]:
                if hash_value == self.capacity[new_index][1] and\
                        self.capacity[new_index][0] == key:
                    if self.capacity[new_index][2] != value:
                        self.capacity[new_index][2] = value
                        break
                elif new_index == self.length_hash - 1:
                    new_index = 0
                else:
                    new_index += 1
            else:
                self.capacity[new_index] = [key, hash_, value]
                self.length_dict += 1
                break

    def __getitem__(self, key):
        hash_ = hash(key)
        new_index = hash_ % self.length_hash
        while True:
            if not self.capacity[new_index]:
                raise KeyError(f"{key} is not founded")
            if self.capacity[new_index] and\
                    self.capacity[new_index][0] == key and\
                    self.capacity[new_index][1] == hash_:
                return self.capacity[new_index][2]
            elif new_index == self.length_hash - 1:
                new_index = 0
            else:
                new_index += 1

    def __len__(self):
        return self.length_dict

    def __delitem__(self, key):
        hash_ = hash(key)
        hash_index = hash_ % len(self.capacity)
        while True:
            if not self.capacity[hash_index]:
                raise KeyError(f"{key} is not founded")
            if self.capacity[hash_index] and \
                    self.capacity[hash_index][1] == hash_ and\
                    self.capacity[hash_index][0] == key:
                pop_item = self.capacity[hash_index]
                self.capacity[hash_index][0] = None
                self.capacity[hash_index][2] = None
                self.length_dict -= 1
                return pop_item
            elif hash_index == self.length_hash - 1:
                hash_index = 0
            else:
                hash_index += 1

    def __repr__(self):
        new_string = []
        if self.length_dict:
            for item in self.capacity:
                if item:
                    new_string.append(f"{item[0]}: {item[2]}")
        return f"{{{', '.join(new_string)}}}"

    def __resize_hash(self):
        temp_capacity = self.capacity.copy()
        self.length_hash *= 2
        self.capacity = [[] for _ in range(self.length_hash)]
        for item in temp_capacity:
            if item and item[0] is not None:
                self.__setitem__(item[0], item[2])
                self.length_dict -= 1
        del temp_capacity

    def get(self, key, default=None):
        try:
            pop_item = self.__getitem__(key)
        except KeyError:
            if default is not None:
                return default
            else:
                raise
        return pop_item

    def pop(self, key, default=None):
        try:
            self.__delitem__(key)
        except KeyError:
            if default is not None:
                return default
            raise

    def update(self, other):
        for item in other:
            if item:
                self.__setitem__(item[0], item[2])

    def clear(self):
        self.length_hash = 8
        self.length_dict = 0
        self.capacity = [[] for _ in range(self.length_hash)]
