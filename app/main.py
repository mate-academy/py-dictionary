class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.length = 0
        self.hash_list = [[]] * self.capacity
        self.threshold = int(self.capacity * 2 / 3)

    def resize(self) -> None:
        self.capacity *= 2
        self.threshold = int(self.capacity * 2 / 3)
        self.length = 0
        old_hash_list = self.hash_list
        self.hash_list = [[]] * self.capacity
        for hash_key_value in old_hash_list:
            if hash_key_value:
                hash_, key, value = hash_key_value
                self.__setitem__(key, value)

    def __setitem__(self, key: any, value: any) -> None:
        if key is None:
            raise KeyError()
        if self.length > self.threshold:
            self.resize()
        current_hash = hash(key)
        index = current_hash % self.capacity
        while True:
            if not self.hash_list[index]:
                self.hash_list[index] = current_hash, key, value
                self.length += 1
                break
            if current_hash == self.hash_list[index][0] \
                    and key == self.hash_list[index][1]:
                self.hash_list[index] = current_hash, key, value
                break
            index = (index + 1) % self.capacity

    def __getitem__(self, key: any) -> any:
        current_hash = hash(key)
        index = current_hash % self.capacity
        while self.hash_list[index]:
            if current_hash == self.hash_list[index][0]\
                    and key == self.hash_list[index][1]:
                return self.hash_list[index][2]
            index = (index + 1) % self.capacity
        raise KeyError()

    def __len__(self) -> any:
        return self.length
