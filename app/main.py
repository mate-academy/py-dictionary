class Dictionary:

    def __init__(self) -> None:
        self.capacity = 8
        self.dictionary = [None] * self.capacity
        self.load_factor = 2 / 3
        self.length = 0

    def __setitem__(self, key: int, value: int) -> None:
        if self.length / self.capacity > self.load_factor:
            self.capacity = self.capacity * 2
            self.new_dictionary = [None] * self.capacity
            for element in self.dictionary:
                if element is not None:
                    old_key = element[0]
                    old_value = element[2]
                    index = hash(element[0]) % self.capacity
                    for i in range(self.capacity):
                        new_index = (index + i) % self.capacity
                        if self.new_dictionary[new_index] is None:
                            self.new_dictionary[new_index] = (
                                old_key, hash(old_key), old_value
                            )
                            break
                        if self.new_dictionary[new_index][0] == old_key:
                            self.new_dictionary[new_index] = (
                                old_key, hash(old_key), old_value
                            )
                            break
            self.dictionary = self.new_dictionary
        index = hash(key) % self.capacity
        for i in range(self.capacity):
            new_index = (index + i) % self.capacity
            if self.dictionary[new_index] is None:
                self.dictionary[new_index] = (key, hash(key), value)
                self.length = self.length + 1
                break
            if self.dictionary[new_index][0] == key:
                self.dictionary[new_index] = (key, hash(key), value)
                break

    def __getitem__(self, key: int) -> None:
        index = hash(key) % self.capacity
        for i in range(self.capacity):
            new_index = (index + i) % self.capacity
            if (self.dictionary[new_index] is not None
                    and key == self.dictionary[new_index][0]):
                return self.dictionary[new_index][2]
            if (self.dictionary[new_index] is not None
                    and key != self.dictionary[new_index][0]):
                continue
            else:
                raise KeyError(f"Key {key} not found")

    def __len__(self) -> int:
        return self.length
