from typing import Any


class Dictionary:
    def __init__(self, bucket: int = 8) -> None:
        self.__bucket = bucket
        self.__table = [[] for _ in range(bucket)]

    def hash_function(self, key: Any) -> int:
        return hash(key) % self.__bucket

    def __setitem__(self, key: int, value: Any) -> None:
        index = self.hash_function(key)
        for idx, pair in enumerate(self.__table[index]):
            if pair[0] == key:
                self.__table[index][idx][1] = value
                return

        self.__table[index].append([key, value])

    def __getitem__(self, key: Any) -> Any:
        index = self.hash_function(key)
        for item in self.__table[index]:
            if item[0] == key:
                return item[1]
        raise KeyError(key)

    def __len__(self) -> int:
        count = 0
        for element in self.__table:
            count += len(element)
        return count

    def __delitem__(self, key: int) -> None:
        index = self.hash_function(key)
        for idx, pair in enumerate(self.__table[index]):
            if pair[0] == key:
                del self.__table[index][idx]
