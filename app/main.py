class Dictionary:
    FILL_RATE = 2/3

    def __init__(self):
        self.cells = 8
        self._dict = [[] for _ in range(self.cells)]
        self.filling = 0

    def __setitem__(self, key, value):
        if self.filling == int(self.cells * self.FILL_RATE):
            self.resize()
        _hash = hash(key)
        cell = _hash % self.cells
        if not self._dict[cell]:
            self._dict[cell] = [key, _hash, value]
            self.filling += 1
        elif self._dict[cell][0] == key:
            self._dict[cell][2] = value
        else:
            cell = (cell + 1) % self.cells
            while True:
                if not self._dict[cell]:
                    self._dict[cell] = [key, _hash, value]
                    self.filling += 1
                    break
                elif self._dict[cell][0] == key:
                    self._dict[cell][2] = value
                    break
                cell = (cell + 1) % self.cells

    def __getitem__(self, key):
        _hash = hash(key)
        cell = _hash % self.cells
        for _ in range(self.cells):
            if self._dict[cell][0] == key:
                return self._dict[cell][2]
            cell = (cell + 1) % self.cells
        raise KeyError

    def resize(self):
        self.cells *= 2
        self.filling = 0
        storage = self._dict[:]
        self._dict = [[] for _ in range(self.cells)]
        for cell in storage:
            if cell:
                self.__setitem__(cell[0], cell[2])

    def __len__(self):
        return self.filling
