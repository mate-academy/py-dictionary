class Dictionary:
    elements = list()

    def __init__(self) -> None:
        self._bucket_size = 8
        self._capacity = 0
        self.elements = [[]] * self._bucket_size

    def __setitem__(self, key: int | str, value: int | str) -> None:
        self._set_value(key, value)

    def __len__(self) -> int:
        return self._capacity

    def __getitem__(self, input_key: str | int) -> str | int:
        hashed_value = hash(input_key)
        index = hashed_value % self._bucket_size
        count = 0
        while count <= self._bucket_size:
            if self.elements[index]:
                key = self.elements[index][0]
                value = self.elements[index][1]
                if key == input_key:
                    return value
            index = (index + 1) % self._bucket_size
            count += 1
        raise KeyError

    def _calculate_capacity(self) -> None:
        if self._capacity > (self._bucket_size * 2 / 3):
            old_elements = self.elements
            self._capacity = 0
            self._bucket_size *= 2
            self.elements = [[]] * self._bucket_size
            for pair in old_elements:
                if pair:
                    self._set_value(pair[0], pair[1])

    def _set_value(self, key: int | str, value: int | str) -> None:
        self._calculate_capacity()
        hash_ = hash(key)
        index = hash_ % self._bucket_size
        if not self.elements[index]:
            self.elements[index] = [key, value, hash_]
            self._capacity += 1
            return
        while self.elements[index]:
            if self.elements[index][0] == key and \
                    self.elements[index][2] == hash_:
                self.elements[index][1] = value
                return
            index = (index + 1) % self._bucket_size
        self.elements[index] = [key, value, hash_]
        self._capacity += 1
