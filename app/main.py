from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.initial_capacity = 8
        self.load_factor = 2 / 3
        self.list_size = 0
        self.buckets_size = self.initial_capacity
        self.list = [[]] * self.initial_capacity

    def check_load_factor(self) -> None:
        current_load = self.list_size / float(self.buckets_size)
        if current_load > self.load_factor:
            self.buckets_size += self.initial_capacity
            self.resize_rehash()

    def generate_new_list(self) -> None:
        self.list_size = 0
        self.list = [[]] * self.buckets_size

    def get_index(self, key: Hashable) -> int:
        index = hash(key) % self.buckets_size
        if self.list[index][0] != key:
            raise IndexError(f"Key {key} not found in")
        return index

    def resize_rehash(self) -> None:
        temp_data = self.list
        self.generate_new_list()
        for bucket_list in temp_data:
            if bucket_list:
                key, index, value = bucket_list
                self.__setitem__(key, value)

    def __getitem__(self, key: Hashable) -> list:
        index = hash(key) % self.buckets_size
        while self.list[index]:
            if self.list[index][0] == key:
                return self.list[index][2]
            index = (index + 1) % self.buckets_size
        raise KeyError

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = hash(key) % self.buckets_size
        while True:
            if not self.list[index]:
                self.list[index] = [key, index, value]
                self.list_size += 1
                self.check_load_factor()
                break
            if self.list[index][0] == key:
                self.list[index][2] = value
                break
            index = (index + 1) % self.buckets_size

    def __delitem__(self, key: Hashable) -> None:
        index = self.get_index(key)
        if self.list[index][0] == key:
            self.list[index].clear()
            self.list_size -= 1

    def pop(self, key: Hashable) -> None:
        index = self.get_index(key)
        value = self.list[index][2]
        self.list[index].clear()
        self.list_size -= 1
        return value

    def __len__(self) -> int:
        return self.list_size

    def get_num_buckets(self) -> int:
        return self.buckets_size

    def clear(self) -> None:
        self.list = [[]] * self.initial_capacity
        self.list_size = 0
