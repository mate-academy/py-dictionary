class Dictionary:
    def __init__(self) -> None:
        self.__capacity = 8
        self.__table = [[] for _ in range(self.__capacity)]
        self.__size = 0
        self.__max_load = 0.7

    def __setitem__(
            self,
            key: str,
            value: any
    ) -> None:
        h = hash(key)
        num_hash = h % self.__capacity
        if len(self.__table[num_hash]) == 0:
            self.__table[num_hash].append((key, h, value))
            self.__size += 1
        else:
            is_editing = False
            for pos, values in enumerate(self.__table[num_hash]):
                if key == values[0]:
                    self.__table[num_hash][pos] = (key, h, value)
                    is_editing = True
                    break

            if not is_editing:
                self.__table[num_hash].append((key, h, value))
                self.__size += 1

        load = self.__size / self.__capacity
        if load > self.__max_load:
            self.__capacity *= 2
            tables = self.__table.copy()
            self.__table = [[] for _ in range(self.__capacity)]

            for list_table in tables:
                for table in list_table:
                    new_hash = table[1] % self.__capacity
                    self.__table[new_hash].append(table)

    def __getitem__(self, key: str) -> tuple:

        h = hash(key)
        index = h % self.__capacity
        for table in self.__table[index]:
            if table[0] == key:
                return table[2]

        raise KeyError(f"key no found: {key}")

    def __len__(self) -> int:
        return self.__size
