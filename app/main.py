class Dictionary:
    def __init__(self) -> None:
        self.size = 8
        self.load = 0
        self.data = [None] * self.size

    def __setitem__(self, key: any, value: any) -> None:
        if self.load < self.size * 2 / 3:
            index = hash(key) % self.size
            if self.data[index] is None:
                self.data[index] = (hash(key), key, value)
                self.load += 1
            elif (self.data[index][0] == hash(key)
                  and self.data[index][1] == key):
                self.data[index] = (hash(key), key, value)
            else:
                for i in range(self.size):
                    if (self.data[i] is not None
                            and self.data[i][0] == hash(key)
                            and self.data[i][1] == key):
                        self.data[i] = (hash(key), key, value)
                        return None
                    if self.data[i] is None:
                        self.data[i] = (hash(key), key, value)
                        self.load += 1
                        return None
        else:
            self.size *= 2
            data_list = self.data.copy()
            self.data = [None] * self.size
            for item in data_list:
                if item is not None:
                    self.__setitem__(item[1], item[2])
            self.__setitem__(key, value)

    def __getitem__(self, key: any) -> any:
        index = hash(key) % self.size
        if self.data[index] is not None and self.data[index][1] == key:
            return self.data[index][2]
        else:
            for item in self.data:
                if (item is not None
                        and item[0] == hash(key)
                        and item[1] == key):
                    return item[2]
        raise KeyError(f"{key} not found")

    def __len__(self) -> int:
        return len([item for item in self.data if item is not None])

    def clear(self) -> None:
        self.size = 8
        self.load = 0
        self.data = [None] * self.size

    def __delitem__(self, key: any) -> None:
        for i in range(self.size):
            if (self.data[i] is not None
                    and self.data[i][0] == hash(key)
                    and self.data[i][1] == key):
                self.data[i] = None
                return None
        raise KeyError(f"{key} not found")

    def get(self) -> list:
        return [{item[1]: item[2]} for item in self.data if item is not None]

    def pop(self, key: any) -> any:
        for i in range(self.size):
            if (self.data[i] is not None
                    and self.data[i][0] == hash(key)
                    and self.data[i][1] == key):
                value = self.data[i][2]
                self.load -= 1
                self.data[i] = None
                return value
        raise KeyError(f"{key} not found")

    def update(self, key: any, value: any) -> None:
        self.__setitem__(key, value)

    def __iter__(self) -> list:
        return [item[1] for item in self.data if item is not None]
