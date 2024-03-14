class Dictionary:

    def __init__(self):
        self.capacity = 8
        self.load_factor = 2 / 3
        self.length = 0
        self.buckets = self.create_table()

    def __setitem__(self, key, value):
        hash_code = hash(key)
        index = int(hash_code % self.capacity)
        if self.length > 0:
            if self.length / self.capacity > self.load_factor:
                self.resize()
        accept = False
        while self.buckets[index][0] is not None:
            if self.buckets[index][1] == key:
                self.buckets[index][2] = value
                accept = True
                break
            index = (index + 1) % self.capacity
        if not accept:
            self.buckets[index] = [hash_code, key, value]
            self.length += 1

    def __getitem__(self, input_key):
        hash_code = hash(input_key)
        index = hash_code % self.capacity
        counter = 0
        while True:
            counter += 1
            try:
                if self.buckets[index][0] is not None:
                    hash_x, key, value = self.buckets[index]
                    if hash_x == hash_code and input_key == key:
                        return value
            except IndexError:
                raise KeyError(input_key)
            if counter == self.capacity:
                break
            index = (index + 1) % self.capacity
        raise KeyError(input_key)

    def __len__(self):
        return self.length

    def resize(self):
        self.capacity *= 2
        copy_elements = self.buckets.copy()
        self.buckets = self.create_table()
        self.length = 0
        for cell in copy_elements:
            if cell[0] is not None:
                self.__setitem__(cell[1], cell[2])
        del copy_elements

    def create_table(self):
        return [[None] for _ in range(self.capacity)]
