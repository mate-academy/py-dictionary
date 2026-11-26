class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.hash_table: list = [None] * 8

    def __len__(self) -> int:
        return self.length

    def __setitem__(self, key: int, value: type) -> None:
        table_index = (hash(key) % len(self.hash_table))
        offset = 0

        for _ in range(len(self.hash_table)):
            indx = (table_index + offset) % len(self.hash_table)
            entry = self.hash_table[indx]
            if entry is None:
                self.hash_table[indx] = [value, key, indx]
                self.length += 1
                self.resize_check()
                break
            if entry[1] == key:
                self.hash_table[indx] = [value, key, indx]
                break
            offset += 1

    def __getitem__(self, key: int) -> object:
        table_index = (hash(key) % len(self.hash_table))

        offset = 0
        try:
            for _ in range(len(self.hash_table)):
                indx = (table_index + offset) % len(self.hash_table)
                entry = self.hash_table[indx]
                if entry is None:
                    raise KeyError
                if entry[1] == key:
                    return entry[0]
                offset += 1
            raise KeyError
        except KeyError:
            raise KeyError("File not found")

    def resize_check(self) -> None:
        bucket_size = len(self.hash_table)
        if self.length >= 2 / 3 * bucket_size:
            temporary_table = [x for x in self.hash_table if x is not None]
            self.hash_table = [None] * (bucket_size * 2)
            self.length = 0

            for item in temporary_table:
                self.__setitem__(item[1], item[0])
