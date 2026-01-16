from typing import Any, Hashable, Union


class Dictionary:

    def __init__(
            self,
            keys: list[Union] = None,
            values: list[Union] = None
    ) -> None:
        if keys is None and values is None:
            keys = []
            values = []
        self.length: int = 0
        self.hash_table: list = [None] * 8
        self.keys = keys
        self.values = values
        self.need_key: Union = None
        for i in range(len(keys)):
            self.__setitem__(keys[i], values[i])

    def __setitem__(self, key_dict: Hashable, value_dict: Any) -> None:
        if (
            self.hash_table.count(None)
            == (
                len(self.hash_table)
                - int(len(self.hash_table) * 2 / 3)
            )
        ):
            copy_old_table = self.hash_table.copy()
            self.hash_table = [None] * len(self.hash_table) * 2
            for cell in copy_old_table:
                if cell:
                    self.need_key = cell[0]
                    self.hash_table[self.__hash__()] = cell
        self.need_key = key_dict
        self.hash_table[self.__hash__()] = [key_dict, value_dict]
        self.length = len(self.hash_table) - self.hash_table.count(None)

    def __getitem__(self, key_dict: Hashable) -> Any:
        self.need_key = key_dict
        if not self.hash_table[self.__hash__()]:
            raise KeyError
        return self.hash_table[self.__hash__()][1]

    def __hash__(self) -> int:
        first_hash = hash(self.need_key) % len(self.hash_table)
        while True:
            if (
                not self.hash_table[first_hash]
                or self.hash_table[first_hash][0] == self.need_key
            ):
                return first_hash
            if first_hash == len(self.hash_table) - 1:
                first_hash = 0
            else:
                first_hash = (first_hash + 1) % len(self.hash_table)

    def __len__(self) -> int:
        return self.length

    def get(self, key_dict: Hashable) -> Any:
        self.need_key = key_dict
        if key_dict in self.hash_table[self.__hash__()]:
            return self.hash_table[self.__hash__()][1]

    def pop(self, key_dict: Hashable) -> Any:
        value_uni = self[key_dict]
        self.hash_table[self.__hash__()] = None
        return value_uni

    def clear(self) -> None:
        self.hash_table = []

    def __iter__(self) -> Union:
        self.current_element = 0
        return self

    def __next__(self) -> Union[int, StopIteration]:
        if self.current_element >= self.length:
            raise StopIteration
        result = [
            value[1] for value in self.hash_table if value
        ][self.current_element]
        self.current_element += 1
        return result


if __name__ == "__main__":
    items = [(1, "one"), (2, "two"), (3, "tree"), (4, "four")]

    dictionary = Dictionary()
    for key, value in items:
        dictionary[key] = value

    for key, value in items:
        print(key, dictionary[key])
