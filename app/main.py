class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = 2 / 3
        self.list = [[] for _ in range(self.capacity)]

    def __setitem__(
            self,
            key: (int, float, str, tuple, bool),
            value: any
    ) -> None:
        if len(self) >= self.capacity * self.load_factor:
            self.increase_capacity()

        key_hash = hash(key) % self.capacity

        if not self.list[key_hash]:  # check if cell is empty
            self.list[key_hash] = [key, value, hash(key)]
            return

        for i in range(len(self.list)):  # check if we have key in self.list
            try:
                if self.list[i][0] == key:
                    self.list[i][1] = value
                    return
            except IndexError:
                pass

        while True:  # find and fill next empty cell
            if key_hash + 1 == self.capacity:
                key_hash = 0
            else:
                key_hash += 1
            if not self.list[key_hash]:
                self.list[key_hash] = [key, value, hash(key)]
                return

    def __getitem__(self, key: (int, float, str, tuple, bool)) -> None:
        for cell in self.list:
            try:
                if key == cell[0]:
                    return cell[1]
            except IndexError:
                pass
        raise KeyError(key)

    def __len__(self) -> int:
        count = 0
        for cell in self.list:
            if cell:
                count += 1
        return count

    def increase_capacity(self) -> None:
        old_list = [char for char in self.list if char]
        self.capacity *= 2
        self.list = [[] for _ in range(self.capacity)]
        for char in old_list:
            self[char[0]] = char[1]
