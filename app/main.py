class Dictionary:
    def __init__(self, elements=None):
        if elements is None:
            elements = []
        self.bucket_size = 8
        while len(elements) * 3 / 2 > self.bucket_size:
            self.bucket_size = self.bucket_size << 1
        self.buckets = [[] for _ in range(self.bucket_size)]
        self._assign_buckets(elements)

    def _assign_buckets(self, elements):
        for key, value in elements:
            if type(key) == int:
                hashed_key = key
            else:
                hashed_key = hash(key)
            index = hashed_key % self.bucket_size
            while len(self.buckets[index]) > 0:
                if key in self.buckets[index][0]:
                    self.buckets[index][0][1] = value
                    self.buckets[index][0][2] = hashed_key
                    return
                else:
                    if index + 1 == self.bucket_size:
                        index = 0
                    else:
                        index += 1
            self.buckets[index].append([key, value, hashed_key])

    def __setitem__(self, key, value):
        elements = [(key, value)]
        self._assign_buckets(elements)
        if self.__len__() * 3 / 2 > self.bucket_size:
            self.__resize__()

    def __getitem__(self, input_key):
        if type(input_key) == int:
            hashed_key = input_key
        else:
            hashed_key = hash(input_key)
        index = hashed_key % self.bucket_size
        while len(self.buckets[index]) > 0:
            if input_key in self.buckets[index][0]:
                return self.buckets[index][0][1]
            else:
                if index + 1 == self.bucket_size:
                    index = 0
                else:
                    index += 1
        raise KeyError

    def __len__(self):
        len_buckets = 0
        for element in self.buckets:
            len_buckets += len(element)
        return len_buckets

    def __resize__(self):
        elements = []
        for element in self.buckets:
            for elm in element:
                elements.append(elm[:-1])
        self.bucket_size *= 2
        self.buckets = [[] for _ in range(self.bucket_size)]
        self._assign_buckets(elements)
