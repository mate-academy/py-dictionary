from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.length = 8
        self.load_factor = 2 / 3
        self.dictionary = [None for _ in range(8)]
        self.insert_elem = 0

    def resize(self) -> None:
        new_dictionary = [None for _ in range(2 * self.length)]
        self.length *= 2
        for element in self.dictionary:
            if element:
                index = element[1] % self.length
                if not new_dictionary[index]:
                    new_dictionary[index] = element
                else:
                    need_space = True
                    while need_space:
                        index = (index + 1) % self.length
                        if not new_dictionary[index]:
                            new_dictionary[index] = element
                            need_space = False
        self.dictionary = new_dictionary

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hash_code = hash(key)
        index = hash_code % self.length

        if self.dictionary[index] is None:
            self.dictionary[index] = (key, hash_code, value)
            self.insert_elem += 1
        elif (hash_code == self.dictionary[index][1]) and (
            key == self.dictionary[index][0]
        ):
            self.dictionary[index] = (key, hash_code, value)
        else:
            need_location = True
            while need_location:
                index = (index + 1) % self.length
                if not self.dictionary[index]:
                    self.dictionary[index] = (key, hash_code, value)
                    need_location = False
                    self.insert_elem += 1
                elif (hash_code == self.dictionary[index][1]) and (
                    key == self.dictionary[index][0]
                ):
                    self.dictionary[index] = (key, hash_code, value)
                    need_location = False
        if self.insert_elem / self.length > self.load_factor:
            self.resize()

    def __len__(self) -> int:
        return self.insert_elem

    def __getitem__(self, key: Hashable) -> Any:
        hash_code = hash(key)
        index = hash_code % self.length
        for i in range(self.length):
            index = (hash_code + i) % self.length
            if self.dictionary[index] is not None:
                if self.dictionary[index][0] == key:
                    return self.dictionary[index][2]
        raise KeyError("There is no such key.")
