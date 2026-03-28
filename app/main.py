from typing import Any


class Empty:
    pass


class Dictionary:
    def __init__(
        self,
        keyname: Any = Empty,
        value: Any = Empty
    ) -> None:
        self.max_len = 8
        self.stored_data = [Empty] * self.max_len
        self.filled_elements = 0
        self.load_capacity = 2 / 3

        if Empty != keyname:
            self.__setitem__(keyname, value)

    def __len__(self) -> int:
        return self.filled_elements

    def __setitem__(self, keyname: Any, value: Any) -> None:
        current_len = self.__len__()

        def loop_set_item(writen_value: list) -> bool:
            item_idx = self.__get_idx_by_key__(
                keyname=writen_value[0],
                find_empty=True
            )
            is_new = self.stored_data[item_idx] == Empty
            self.stored_data[item_idx] = writen_value

            return is_new

        if current_len + 1 > self.max_len * self.load_capacity:
            self.max_len *= 2
            all_items = [item for item in self.stored_data if item != Empty]
            self.stored_data = [Empty] * self.max_len

            for keyname_item, saved_hash, value_item in all_items:
                loop_set_item(
                    writen_value=[keyname_item, saved_hash, value_item]
                )

        key_hash = hash(keyname)
        is_new = loop_set_item(writen_value=[keyname, key_hash, value])
        if is_new:
            self.filled_elements += 1

    def __get_idx_by_key__(
        self,
        keyname: Any,
        find_empty: bool = False
    ) -> Any:
        key_hash = hash(keyname)
        curr_idx = key_hash % self.max_len or 0

        for _ in range(self.max_len):
            if (
                Empty == self.stored_data[curr_idx]
                or self.stored_data[curr_idx][0] == keyname
            ) and find_empty:
                return curr_idx
            elif (
                (Empty != self.stored_data[curr_idx])
                and self.stored_data[curr_idx][0] == keyname
                and not find_empty
            ):
                return curr_idx
            else:
                if curr_idx + 1 >= self.max_len:
                    curr_idx = 0
                else:
                    curr_idx += 1

        raise KeyError(f"No key {keyname} in Dictionary")

    def __getitem__(self, keyname: Any) -> Any:
        return self.stored_data[self.__get_idx_by_key__(keyname)][2]

    def items(self) -> Any:
        return [
            (keyname, value)
            for keyname, _, value in [
                item for item in self.stored_data if item != Empty
            ]
        ]

    def keys(self) -> Any:
        return [
            keyname
            for keyname, _, _ in
            [item for item in self.stored_data if item != Empty]
        ]

    def values(self) -> Any:
        return [
            value
            for _, _, value in
            [item for item in self.stored_data if item != Empty]
        ]

    def clear(self) -> None:
        self.__init__()

    def __delitem__(self, key: Any) -> None:
        self.stored_data[self.__get_idx_by_key__(key)] = Empty
        self.filled_elements -= 1

    def pop(self, keyname: Any, defaultvalue: Any = None) -> Any:
        try:
            key_idx = self.__get_idx_by_key__(keyname)
            deleted_value = self.stored_data[key_idx][2]
            self.stored_data[key_idx] = Empty
            self.filled_elements -= 1

            return deleted_value
        except KeyError:
            return defaultvalue

    def get(self, keyname: Any, defaultvalue: Any = None) -> Any:
        try:
            return self.__getitem__(keyname)
        except KeyError:
            return defaultvalue

    def update(self, *args, **kargs) -> None:
        for keyname, value in kargs.items():
            self.__setitem__(keyname, value)

        for argument in args:
            item_items = getattr(argument, "items", None)

            if item_items is not None and callable(item_items):
                for keyname, value in argument.items():
                    self.__setitem__(keyname, value)
            else:
                try:
                    for keyname, value in argument:
                        self.__setitem__(keyname, value)
                except ValueError as e:
                    print(e)

    def __iter__(self) -> Any:
        for keyname in self.keys():
            yield keyname
