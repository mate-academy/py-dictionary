class Dictionary:
    def __init__(self):
        self.capacity = 8
        self.load_factor = int(self.capacity / 3 * 2)
        self.full_spaces = 0
        self.elements = []
        self.dictionary = [[] for _ in range(self.capacity)]

    def resize(self):
        self.capacity = self.capacity * 2
        self.load_factor = int(self.capacity / 3 * 2)
        self.clear()
        self.dictionary = self.dictionary + [[] for _ in
                                             range(self.capacity)]
        self.full_spaces = 0
        elements = self.elements[:]
        self.elements = []
        for (k, v) in elements:
            self.__setitem__(k, v)
        return [self.capacity, self.load_factor]

    def checking_free_spaces(self):
        if self.full_spaces == self.load_factor:
            self.resize()

    def __setitem__(self, key, value):
        if not isinstance(key, (list, dict, set)):
            hashed_key = hash(key)
            key_index = hashed_key % self.capacity
            while True:
                is_list_empty = len(self.dictionary[key_index])
                if is_list_empty == 0:
                    self.dictionary[key_index].append(key)
                    self.dictionary[key_index].append(value)
                    self.elements.append([key, value])
                    self.full_spaces += 1
                    self.checking_free_spaces()
                    return
                else:
                    if self.dictionary[key_index][0] == key:
                        self.dictionary[key_index][1] = value
                        for element in self.elements:
                            if element[0] == key:
                                element[1] = value
                        return
                    elif key_index + 1 == len(self.dictionary):
                        key_index = 0
                    else:
                        key_index += 1
        else:
            raise KeyError

    def __getitem__(self, input_key):
        hashed_key = hash(input_key)
        key_index = hashed_key % self.capacity
        total_loops = self.full_spaces
        while total_loops != 0:
            if len(self.dictionary[key_index]) == 0:
                raise KeyError(input_key)
            key_ = self.dictionary[key_index][0]
            if key_ == input_key:
                return self.dictionary[key_index][1]
            elif key_index == len(self.dictionary) - 1:
                key_index = 0
                total_loops -= 1
            else:
                key_index += 1
                total_loops -= 1

        raise KeyError

    def __len__(self):
        return self.full_spaces

    def clear(self):
        return self.dictionary.clear()

    def get(self, key):
        return self.__getitem__(key)
