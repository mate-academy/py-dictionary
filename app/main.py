class Dictionary:
    __START_CAPACITY = 8
    __RESIZE_VALUE = 2
    __TRASHOLD = 2 / 3

    def __init__(self):
        self.__capacity = self.__START_CAPACITY
        self.__hash_table = self.__create_empty_hash_table(self.__capacity)
        self.__number_of_elements = 0

    def __create_empty_hash_table(self, capacity):
        return [None for _ in range(capacity)]

    def __resize(self):
        self.__current_elements = [
            cell
            for cell in self.__hash_table
            if cell is not None
        ]
        self.__capacity *= self.__RESIZE_VALUE
        self.__hash_table = self.__create_empty_hash_table(self.__capacity)
        self.__number_of_elements = 0
        for cell in self.__current_elements:
            self.__setitem__(cell[0], cell[1])

    def __setitem__(self, key, value):
        if (self.__number_of_elements + 1) > self.__capacity * self.__TRASHOLD:
            self.__resize()

        hash_ = hash(key)
        index_ = hash_ % self.__capacity
        cell = [key, value, hash_]

        while self.__hash_table[index_] is not None:
            if self.__hash_table[index_][2] == hash_ and \
                    self.__hash_table[index_][0] == key:
                self.__hash_table[index_][1] = value
                return

            index_ = (index_ + 1) % self.__capacity

        self.__hash_table[index_] = cell
        self.__number_of_elements += 1

    def __getitem__(self, item):
        hash_ = hash(item)
        index_ = hash_ % self.__capacity

        while self.__hash_table[index_] is not None:
            if self.__hash_table[index_][2] == hash_ and \
                    self.__hash_table[index_][0] == item:
                return self.__hash_table[index_][1]

            index_ = (index_ + 1) % self.__capacity
        raise KeyError(f"{item} does not exist")

    def __len__(self):
        return self.__number_of_elements
