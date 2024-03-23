from typing import Any, Hashable, Optional


class Dictionary:

    __load_factor: float = 0.66

    def __init__(self) -> None:
        self.__capacity: int = 8
        self.__hash_table: list[Optional[tuple[Hashable, int, Any]]] = [
            None for _ in range(self.__capacity)
        ]
        self.__index_of_cell: int
        self.__index_of_iteration: int

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.__len__() > self.__capacity * self.__load_factor:
            self.__resize_hash_table()

        self.__put_item_to_hash_table(key=key, hash_inf=hash(key), value=value)

    def __delitem__(self, key: Hashable) -> None:
        del_item_index = self.__hash_table.index(self.__find_item(key=key))
        self.__hash_table[del_item_index] = None

    def __getitem__(self, key: Hashable) -> Any:
        return self.__find_item(key)[2]

    def keys(self) -> list:
        return [cell[0] for cell in self.__hash_table if cell]

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self.__find_item(key=key)[2]

        except KeyError:
            return default

    def pop(self, key: Hashable, default: Any = None) -> Any:
        try:
            item = self.__find_item(key=key)
            value = item[2]
            self.__delitem__(item[0])
            return value

        except KeyError:

            if default is None:
                raise KeyError
            return default

    def update(self, other: "Dictionary") -> None:

        for cell in other.__hash_table:
            if cell:
                key, hash_inf, value = cell
                self.__setitem__(key=key, value=value)

    def __len__(self) -> int:
        return sum(1 for cell in self.__hash_table if cell)

    def clear(self) -> None:
        self.__capacity = 8
        self.__hash_table = [None for _ in range(self.__capacity)]

    def __resize_hash_table(self) -> None:
        old_hash_table = self.__hash_table

        self.__capacity *= 2
        self.__hash_table = [() for _ in range(self.__capacity)]

        for cell in old_hash_table:
            if cell:
                self.__put_item_to_hash_table(*cell)

    def __find_item(self, key: Hashable) -> tuple:
        if key not in self.keys():
            raise KeyError

        self.__index_of_cell = self.__get_index_for_hash_table(key)

        while True:

            if key == self.__hash_table[self.__index_of_cell][0]:
                return self.__hash_table[self.__index_of_cell]

            self.__index_of_cell = (
                self.__index_of_cell + 1
            ) % self.__capacity

    def __get_index_for_hash_table(self, key: Hashable) -> int:
        return hash(key) % self.__capacity

    def __put_item_to_hash_table(
        self, key: Hashable, hash_inf: int, value: Any
    ) -> None:
        self.__index_of_cell = self.__get_index_for_hash_table(key=key)

        while True:

            if (
                not self.__hash_table[self.__index_of_cell]
                or key == self.__hash_table[self.__index_of_cell][0]
            ):
                self.__hash_table[self.__index_of_cell] = (
                    key, hash_inf, value
                )
                break

            self.__index_of_cell = (
                self.__index_of_cell + 1
            ) % self.__capacity

    def __iter__(self) -> "Dictionary":
        self.__index_of_iteration = 0
        return self

    def __next__(self) -> Hashable:
        if self.__index_of_iteration >= self.__len__():
            raise StopIteration

        result = self.__hash_table[self.__index_of_iteration][0]
        self.__index_of_iteration += 1

        return result
