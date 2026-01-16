class Dictionary:
    def __init__(self):
        self.__capacity = 8
        self.__size = 0
        self.__memory: list = [None] * 8
        self.__current_element = []

    def __setitem__(self, key, value):
        self.resize_dictionary()
        self.__add_new_element(key, value)

    def resize_dictionary(self):
        if self.__size == int(self.__capacity * 2 / 3):
            self.__capacity *= 2
            self.__current_element = [el for el in self.__memory]
            self.__memory = [None] * self.__capacity
            self.__size = 0
            for element in self.__current_element:
                if element is not None:
                    self.__add_new_element(element[0], element[1])

    def __add_new_element(self, key, value):
        hash_ = hash(key)
        memory_place_ = hash_ % self.__capacity
        if self.__memory[memory_place_] is not None:
            while True:
                if memory_place_ == self.__capacity:
                    memory_place_ = 0

                if self.__memory[memory_place_] is None:
                    self.__memory[memory_place_] = (key, value, hash_)
                    self.__size += 1
                    break

                if self.__memory[memory_place_] is not None and (
                    key == self.__memory[memory_place_][0]
                ):
                    self.__memory[memory_place_] = (key, value, hash_)
                    break

                memory_place_ += 1
        else:
            self.__memory[memory_place_] = (key, value, hash_)
            self.__size += 1

    def __getitem__(self, item):
        hash_ = hash(item)
        index_ = hash_ % self.__capacity

        for _ in range(self.__capacity):
            if self.__memory[index_] is not None and (
                    self.__memory[index_][0] == item):
                return self.__memory[index_][1]
            index_ = (index_ + 1) % self.__capacity
        else:
            raise KeyError(f"Key: {item} not in dictionary!")

    def __len__(self):
        return self.__size
