class Dictionary:
    def __init__(self):
        self.dict_len = 8
        self.length = 0
        self.element = [None] * self.dict_len

    def __setitem__(self, key, value):
        if len(self) == int(self.dict_len * 2 / 3):
            self.resize()

        hash_key = hash(key)
        new_el = (hash_key, key, value)  # store: hash, key, value
        i = hash_key % self.dict_len

        while True:
            if self.element[i] is None:
                self.element[i] = new_el
                self.length += 1
                break
            elif hash_key == self.element[i][0] and key == self.element[i][1]:
                self.element[i] = new_el
                break
            else:
                i = (i + 1) % self.dict_len

    def __getitem__(self, key):
        hash_key = hash(key)
        i = hash_key % self.dict_len

        while True:
            if self.element[i] is None:
                raise KeyError

            if self.element[i][0] == hash_key and key == self.element[i][1]:
                return self.element[i][2]
            else:
                i = (i + 1) % self.dict_len

    def __len__(self):
        return self.length

    def resize(self):
        self.dict_len *= 2
        self.length = 0
        old_dict, self.element = self.element, [None] * self.dict_len

        for el in old_dict:
            if el is not None:
                self.__setitem__(el[1], el[2])
