from typing import Any


class Dictionary:

    def __init__(self) -> None:
        self.index_key = None
        self.my_dict = ["", "", "", "", "", "", "", "", ]
        self.max_length = 8
        self.max_items = self.max_length * 2 // 3
        self.count_items = 0

    def __setitem__(self, key: Any, value: Any) -> None:
        self.hash_key = hash(key)
        self.index_key = self.hash_key % self.max_length

        if self.check_item(self.hash_key, key):
            self.update(self.hash_key, key, value)
        else:
            if self.count_items >= self.max_items:
                self.old_list = self.reset_dict()
                self.old_list.append((self.hash_key, key, value))
                for item in self.old_list:
                    if item != "":
                        self.add_new_item(*item)
            else:
                self.add_new_item(self.hash_key, key, value)

    def __getitem__(self, key: Any) -> Any:
        try:
            self.index_key = hash(key) % self.max_length
            if self.check_item(hash(key), key):
                return self.my_dict[self.index_key][2]
            else:
                raise KeyError
        except IndexError:
            raise KeyError(key)

    def __len__(self) -> int:
        return self.count_items

    def add_new_item(
            self,
            hash_key: int,
            key: Any,
            value: Any
    ) -> None:
        self.index_key = hash_key % self.max_length
        self.check_item(hash_key, key)
        self.count_items += 1
        self.my_dict[self.index_key] = (hash_key, key, value)

    def reset_dict(self) -> list:
        self.index_key = None
        self.max_length *= 2
        self.max_items = self.max_length * 2 // 3
        self.count_items = 0
        old_dict = self.my_dict.copy()
        self.my_dict = [""] * self.max_length
        return old_dict

    def check_item(self, hash_key: int, key: Any) -> bool:
        self.check_index = self.index_key
        while True:
            if self.my_dict[self.index_key] == "":
                return False
            elif (self.my_dict[self.index_key][1] == key
                  and self.my_dict[self.index_key][0] == hash_key):
                return True
            self.index_key = (self.index_key + 1) % self.max_length
            if self.check_index == self.index_key:
                return False

    def update(self, hash_key: int, key: Any, value: Any) -> None:
        self.my_dict[self.index_key] = (hash_key, key, value)
