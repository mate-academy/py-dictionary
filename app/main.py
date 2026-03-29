import random
from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.hash_table: list = [None] * 8
        self.lenght = 0

    @staticmethod
    def count_of_elements(ls: list) -> int:
        return sum(1 for element in ls if element is not None)

    @staticmethod
    def get_keys_from_hash_table(hash_list: list[tuple | None]) -> list:
        return [item[0] for item in hash_list if item is not None]

    def collision(self,
                  index: int,
                  ls: list,
                  key: Hashable = 0,
                  value: Any = 0) -> None:
        index = random.choice(
            [i for i in range(len(ls))
                if ls[i] is None])
        ls[index] = (key, value)

    def __len__(self) -> int:
        return self.lenght

    def __setitem__(self, key: Hashable, value: Any) -> None:
        threshhold = int(len(self.hash_table) * (2 / 3))
        hash_key = self.__hash__(key)
        if threshhold > self.count_of_elements(self.hash_table):
            index = hash_key % len(self.hash_table)
            if all(x is None for x in self.hash_table):
                self.hash_table[index] = (key,
                                          value,
                                          hash_key)
                self.lenght += 1
            # update value if key is equal
            elif any(
                item is not None
                and item[0] == key for item in self.hash_table
            ):
                self.update(key, value)
            elif self.hash_table[index] is None:
                self.hash_table[index] = (key,
                                          value,
                                          hash_key)
                self.lenght += 1
            else:
                # If we have collision
                self.collision(index, self.hash_table, key, value)
                self.lenght += 1
        else:
            # if we need to resize hash table
            temp_list = [None] * (len(self.hash_table) * 2)
            for element in self.hash_table:
                if element is None:
                    continue
                else:
                    idx = hash(element[0]) % len(temp_list)
                    if temp_list[idx] is None:
                        temp_list[idx] = element
                    else:
                        # if we have collision
                        self.collision(idx, temp_list, element[0], element[1])
            # add new element in hash table after resize
            self.hash_table = temp_list
            self.lenght = self.count_of_elements(self.hash_table)
            index = hash_key % len(self.hash_table)
            if self.hash_table[index] is None:
                self.hash_table[index] = (key,
                                          value,
                                          hash_key)
                self.lenght += 1
            elif key not in self.get_keys_from_hash_table(self.hash_table):
                self.collision(index, self.hash_table, key, value)
                self.lenght += 1
            else:
                self.update(key, value)

    def __getitem__(self, key: Hashable) -> Any:
        if len(self.hash_table) == 0:
            raise KeyError(key)
        hash_key = self.__hash__(key)
        start_index = hash_key % len(self.hash_table)
        for i in range(len(self.hash_table)):
            current_index = (start_index + i) % len(self.hash_table)
            element = self.hash_table[current_index]
            if element is not None:
                if key == element[0]:
                    return element[1]
        raise KeyError(key)

    def __hash__(self, value: Any) -> int:
        return hash(value)

    def __eq__(self, other: list[tuple]) -> bool:
        for i in range(len(self.hash_table)):
            if (
                self.hash_table[i][0] != other[i][0]
                or self.hash_table[i][1] != other[i][1]
                or self.hash_table[i][2] != other[i][2]
            ):
                return False
        return True

    def clear(self) -> None:
        self.hash_table = [None] * 8
        self.lenght = 0

    def __delitem__(self, key: Hashable) -> None:
        for item in self.hash_table:
            if item[0] == key:
                self.hash_table.remove(item)

    def pop(self, key: Hashable) -> Any | None:
        for i, item in enumerate(self.hash_table):
            if item[0] == key:
                return self.hash_table.pop(i)

    def update(self, key: Hashable, value: Any) -> list:
        hash_key = self.__hash__(key)
        if key in self.get_keys_from_hash_table(self.hash_table):
            for i, item in enumerate(self.hash_table):
                if item and item[0] == key:
                    self.hash_table[i] = (key,
                                          value,
                                          hash_key)
                    break
        return self.hash_table

    def __iter__(self) -> Any:
        for key in self.hash_table:
            if key is None:
                continue
            else:
                yield key[0]
