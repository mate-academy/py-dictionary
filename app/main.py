class Dictionary:
    def __init__(self):
        self.capacity = 8
        self.load_factor = 0
        self.table = [None] * self.capacity

    def __setitem__(self, key, value):
        this_hash = hash(key)
        index = this_hash % self.capacity
        if self.table[index] is None:  # if this cell is empty
            self.table[index] = [this_hash, key, value]
        elif key == self.table[index][1]:  # if this key already exists
            self.table[index] = [this_hash, key, value]
        else:  # if this cell is busy
            while self.table[index] is not None:  # search for free cell
                if index == self.capacity - 1:
                    index = 0
                    continue
                index += 1
            self.table[index] = [this_hash, key, value]
        self.control_capacity()

    def __getitem__(self, key):
        index = hash(key) % self.capacity  # find an index to start with
        while self.table[index]:  # search in all non-empty cells
            this_hash, this_key, _ = self.table[index]
            if this_hash == hash(key):
                if this_key == key:
                    return self.table[index][2]
            index += 1
            if index >= self.capacity - 1:
                index = 0
        raise KeyError

    def __len__(self):
        return len(self.table) - self.table.count(None)

    def control_capacity(self):
        if self.__len__() > 0.66 * self.capacity:
            self.resize()

    def resize(self):
        self.capacity *= 2
        old_table = self.table
        self.table = self.table = [None] * self.capacity
        for cell in old_table:
            if cell:
                self.__setitem__(cell[1], cell[2])
