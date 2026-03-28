class Dictionary:
    def __init__(self):
        self.capacity = 8
        self.dictionary = [None] * self.capacity



    def __setitem__(self, key, value):
        index = hash(key) % self.capacity
        if self.dictionary[index] is None:
            self.dictionary[index] = []
        for i, (k, v) in enumerate(self.dictionary[index]):
            if k == key:
                self.dictionary[index][i] = (key, value)
                return
        self.dictionary[index].append((key, value))


    def __getitem__(self, key):
        index = hash(key) % self.capacity
        if self.dictionary[index] is None:
            raise KeyError
        for i, (k, v) in enumerate(self.dictionary[index]):
            if k == key:
                return v
        raise KeyError


    def __len__(self):
        count = 0
        for i in self.dictionary:
            if i is not None:
                count += len(i)
        return count
