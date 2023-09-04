from typing import Any, Hashable


class Dictionary:
    __items: list[tuple | None]
    __current_len: int = 0

    def __init__(
        self,
        args: list[tuple[Any, Any] | list[Any, Any]] | None = None
    ) -> None:
        self.__items = []
        for _ in range(8):
            self.__items.append(None)

        if args:
            for arg in args:
                if len(arg) == 2:
                    self.__setitem__(arg[0], arg[1])
                else:
                    raise ValueError(
                        f"Dictionary update sequence element #0 has "
                        f"length {len(arg)}; 2 is required"
                    )

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.__check_load_factor():
            self.__resize()
        self.__setitem(key, value)

    def __getitem__(self, key: Hashable) -> Any:
        current_index = self.__find_item_index_by_key(key)
        return self.__items[current_index][1]

    def __len__(self) -> int:
        return self.__current_len

    def __resize(self) -> None:
        new_items = []
        for _ in range(len(self.__items) * 2):
            new_items.append(None)

        current_items = self.items()
        self.__items = new_items
        self.__current_len = 0
        for key, value in current_items:
            self.__setitem(key, value)

    def __check_load_factor(self) -> bool:
        length = len(self.__items)
        load_factor = round(length * (2 / 3) + 1)
        return self.__current_len == load_factor

    def items(self) -> list:
        return [item for item in self.__items if item is not None]

    def __setitem(self, key: Hashable, value: Any) -> None:
        current_index = self.__get_index_from_hash(key)

        while True:
            if not self.__items[current_index]:
                self.__items[current_index] = (key, value)
                self.__current_len += 1
                return
            elif self.__items[current_index][0] == key:
                self.__items[current_index] = (key, value)
                return
            else:
                current_index += 1
                if current_index == len(self.__items):
                    current_index = 0

    def __repr__(self) -> str:
        dict_str_list: list[str] = []
        for key, value in self.items():
            if isinstance(value, str):
                dict_str_list.append(f"{key}: '{value}'")
            else:
                dict_str_list.append(f"{key}: {value}")

        dict_str = ", ".join(dict_str_list)
        return f"{{{dict_str}}}"

    def clear(self) -> None:
        self.__items = []
        self.__current_len = 0

    def __delitem__(self, key: Hashable) -> None:
        current_index = self.__find_item_index_by_key(key)
        self.__del_item_by_index(current_index)

    def __del_item_by_index(self, current_index: int) -> None:
        self.__current_len -= 1
        self.__items[current_index] = None

    def __get_index_from_hash(self, key: Hashable) -> int:
        key_hash = hash(key)
        length = len(self.__items)
        return key_hash % length

    def __find_item_index_by_key(self, key: Hashable) -> int:
        current_index = self.__get_index_from_hash(key)
        begin_index = None
        while True:
            if (
                    self.__items[current_index] is not None
                    and self.__items[current_index][0] == key
            ):
                return current_index
            else:
                if begin_index is None:
                    begin_index = current_index
                elif begin_index == current_index:
                    raise KeyError(
                        f"Dictionary with key '{key}' is not exists"
                    )
                current_index += 1
                if current_index == len(self.__items):
                    current_index = 0

    def get(self, key: Hashable) -> Any:
        return self.__getitem__(key)

    def pop(self, key: Hashable) -> Any:
        current_index = self.__find_item_index_by_key(key)
        item_value = self.__items[current_index][1]
        self.__del_item_by_index(current_index)
        return item_value

    def update(self, other_dict: Any) -> None:
        if isinstance(other_dict, Dictionary):
            other_dict = other_dict.items()

        for key, value in other_dict:
            self.__setitem__(key, value)
