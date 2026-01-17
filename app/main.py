class Dictionary:

    def __init__(self):
        self.__capacity = 8
        self.__dict_with_data = [None] * self.__capacity
        self.__elements = 0

    def __setitem__(self, key, value):
        self.__change_capacity()
        self.__add_data(key, value)

    def __change_capacity(self):
        if self.__elements == int(self.__capacity * 2 / 3):
            self.__capacity *= 2
            current_data = [data for data in self.__dict_with_data
                            if data is not None]
            self.__dict_with_data = [None] * self.__capacity
            self.__elements = 0
            for key, value, hash_ in current_data:
                self.__add_data(key, value)

    def __add_data(self, key, value):
        hash_ = hash(key)
        dict_index = hash_ % self.__capacity

        while True:
            if self.__dict_with_data[dict_index] is None:
                self.__dict_with_data[dict_index] = [key, value, hash_]
                self.__elements += 1
                break
            if self.__dict_with_data[dict_index][0] == key \
                    and hash_ == hash(key):
                self.__dict_with_data[dict_index][1] = value
                break
            dict_index = (dict_index + 1) % self.__capacity

    def __getitem__(self, key):
        hash_ = hash(key)
        index = hash_ % self.__capacity
        while self.__dict_with_data[index] is not None:
            if self.__dict_with_data[index][0] == key and hash_ == hash(key):
                return self.__dict_with_data[index][1]
            index = (index + 1) % self.__capacity
        raise KeyError('Not found')

    def __len__(self):
        return self.__elements
