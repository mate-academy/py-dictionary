from typing import Any


class Dictionary:
    count_value_in_dict = 0

    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.dict = [[] for _ in range(self.capacity)]

    def __setitem__(self, key: Any, value: Any) -> None:
        flag = True
        hash_key = hash(key) % self.capacity
        if self.dict[hash_key]:
            for val_in_dict in self.dict[hash_key]:
                if key in val_in_dict:
                    val_in_dict[1] = value
                    flag = False
        if flag:
            self.dict[hash_key].append([key, value])
            self.count_value_in_dict += 1
            if self.count_value_in_dict >= round(self.capacity * 2 / 3):
                self.resize()

    def resize(self) -> None:
        self.capacity *= 2
        new_dict = [[] for _ in range(self.capacity)]
        for value in self.dict:
            if value:
                for key_value in value:
                    new_dict[
                        hash(key_value[0]) % self.capacity
                    ].append(key_value)
        self.dict = new_dict

    def __getitem__(self, item: Any) -> Any:
        hash_key = hash(item) % self.capacity
        if not self.dict[hash_key]:
            raise KeyError
        for key_value in self.dict[hash_key]:
            if item in key_value:
                return key_value[1]

    def __len__(self) -> int:
        return self.count_value_in_dict
