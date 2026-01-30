class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.threshold = 5
        self.size = 0
        self.dictionary = [None] * self.capacity

    def calculation_algorithm(self, key: str | int, value: str | int) -> None:
        index = hash(key) % self.capacity
        for i in range(self.capacity):
            probe = (index + i) % self.capacity
            item = self.dictionary[probe]
            if item is None:
                self.dictionary[probe] = [key, hash(key), value]
                self.size += 1
                return
            if item[0] == key:
                item[2] = value
                return

    def __setitem__(self, key: str | int, value: str | int) -> None:
        if self.size <= self.threshold:
            self.calculation_algorithm(key, value)
        elif self.size > self.threshold:
            self.dictionary += [None] * self.capacity
            temp = []
            for item in self.dictionary:
                if item is not None:
                    temp.append(item)
            self.capacity = self.capacity * 2
            self.dictionary = [None] * self.capacity
            self.threshold = 2 * self.capacity // 3
            for temp_item in temp:
                self.calculation_algorithm(temp_item[0], temp_item[2])
            self.calculation_algorithm(key, value)

    def __getitem__(self, key: str | int) -> None:
        index = hash(key) % self.capacity
        for i in range(self.capacity):
            probe = (index + i) % self.capacity
            item = self.dictionary[probe]
            if item is None:
                break
            if item[0] == key:
                return item[2]
        raise KeyError("Key outside the dictionary!")

    def __len__(self) -> int:
        return len([i for i in self.dictionary if i is not None])

    def __repr__(self) -> str:
        return f"{{{[key_value for key_value in self.dictionary]}}}"
