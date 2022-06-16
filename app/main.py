class Dictionary:
    def __init__(self):
        self.volume = 0
        self.size = 8
        self.table = [None] * self.size

    def __setitem__(self, key, value):
        i = hash(key) % self.size
        while True:
            if self.table[i] is None:
                self.table[i] = [hash(key), key, value]
                self.volume += 1
                break
            if self.table[i][1] == key:
                self.table[i][2] = value
                break
            i = (i + 1) % self.size
        if self.volume > int(self.size * 2 / 3):
            self.resize()

    def __getitem__(self, key):
        i = hash(key) % self.size
        while self.table[i]:
            if self.table[i][0] == hash(key) and \
                    self.table[i][1] == key:
                return self.table[i][2]
            i = (i + 1) % self.size
        raise KeyError

    def resize(self):
        self.volume = 0
        self.size *= 2
        prev_table = [cell for cell in self.table if cell]
        self.table = [None] * self.size
        for hsh, key, value in prev_table:
            self.__setitem__(key, value)

    def __len__(self):
        return self.volume
