class Dictionary:
    def __init__(self):
        self.__filling = 0
        self.__capacity = 8
        self.__list = [None for _ in range(self.__capacity)]

    def __getitem__(self, key):
        hash_ = hash(key)
        index_ = hash_ % self.__capacity

        while True:
            if not self.__list[index_]:
                raise KeyError(f"Does not exist item with key {key}")
            if self.__list[index_][0] == key:
                return self.__list[index_][1]

            index_ = (index_ + 1) % self.__capacity

    def __setitem__(self, key, value, hash_=None):
        if self.__filling == round(self.__capacity * 2 / 3):
            self.resize()

        hash_ = hash(key)
        index_ = hash_ % self.__capacity

        while True:
            if self.__list[index_] is None:
                self.__list[index_] = (key, value, hash_)
                break
            elif self.__list[index_][0] == key:
                self.__list[index_] = (key, value, hash_)
                self.__filling -= 1
                break
            index_ = (index_ + 1) % self.__capacity
        self.__filling += 1

    def __len__(self):
        return self.__filling

    def resize(self):
        temp_list = [el for el in self.__list if el]
        self.__capacity *= 2
        self.__list = [None for _ in range(self.__capacity)]
        self.__filling = 0
        for item in temp_list:
            self.__setitem__(item[0], item[1], item[2])
