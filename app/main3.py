from typing import Any


class Dictionary:
    def __init__(self, bucket: int = 8) -> None:
        self.__bucket = bucket
        self.__table = [[] for _ in range(bucket)]
        self.length = 0

    def __len__(self) -> int:
        return self.length  # O(1)

    def hashfunction(self, key: Any) -> tuple[int, int]:
        hash_key = hash(key)
        index = hash_key % self.__bucket
        return hash_key, index

    def _insert_no_resize(self, key: Any, hash_key: int, value: Any) -> None:
        lst = [key, hash_key, value]
        index = hash_key % self.__bucket

        if not self.__table[index]:
            self.__table[index].append(lst)
            self.length += 1
            return

        for i, existing in enumerate(self.__table[index]):
            if existing[0] == key:
                self.__table[index][i] = lst
                return

        self.__table[index].append(lst)
        self.length += 1

    def resize(self) -> None:
        threshold = (2 * self.__bucket) // 3
        if self.length >= threshold:
            old_table = self.__table
            self.__bucket *= 2
            self.__table = [[] for _ in range(self.__bucket)]
            self.length = 0

            for slot in old_table:
                for lst in slot:
                    self._insert_no_resize(lst[0], lst[1], lst[2])

    def __setitem__(self, key: Any, value: Any) -> None:
        self.resize()
        hash_key, index = self.hashfunction(key)
        lst = [key, hash_key, value]

        if not self.__table[index]:
            self.__table[index].append(lst)
            self.length += 1
            return

        for i, existing in enumerate(self.__table[index]):
            if existing[0] == key:
                self.__table[index][i] = lst
                return

        self.__table[index].append(lst)
        self.length += 1

    def __getitem__(self, key: Any) -> Any:
        hash_key, index = self.hashfunction(key)
        for lst in self.__table[index]:
            if lst[0] == key:
                return lst[2]

        raise KeyError(f"Key '{key}' not found")
