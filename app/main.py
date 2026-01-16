from __future__ import annotations
from typing import Union, Any


class Dictionary:
    def __init__(self) -> None:
        self.__length = 0
        self.__hash_table = [None] * 8

    @staticmethod
    def hashing_key(
        key: Union[
            int, float, bytes, frozenset, str, bool, complex, tuple, type(None)
        ],
    ) -> int:
        try:
            key_hash = hash(key)
            return key_hash
        except TypeError:
            raise KeyError(
                "Dictionary key must be immutable type \
                and contain only immutable types"
            )

    @staticmethod
    def table_setter_collision_checker(
        dict_list: list, list_index: int, content: tuple
    ) -> bool:
        while True:
            if (
                dict_list[list_index] is None
                or dict_list[list_index] == "__TOMBSTONE"
            ):
                dict_list[list_index] = content
                return False
            if dict_list[list_index][0] == content[0]:
                dict_list[list_index] = content
                return True
            list_index += 1
            if list_index == len(dict_list):
                list_index = 0

    @staticmethod
    def value_finder_by_key(
        dict_list: list,
        list_index: int,
        key: Union[
            int, float, bytes, frozenset, str, bool, complex, tuple, type(None)
        ],
        del_flag: bool = False,
    ) -> Any:
        while dict_list[list_index] is not None:
            if (
                dict_list[list_index] != "__TOMBSTONE"
                and dict_list[list_index][0] == key
            ):
                result = dict_list[list_index]
                if del_flag:
                    dict_list[list_index] = "__TOMBSTONE"
                return result
            list_index += 1
            if list_index == len(dict_list):
                list_index = 0
        raise KeyError(f"Key not found: {key}")

    def __setitem__(
        self,
        key: Union[
            int, float, bytes, frozenset, str, bool, complex, tuple, type(None)
        ],
        value: Any,
    ) -> None:
        key_hash = Dictionary.hashing_key(key)
        self.__length += 1
        if len(self.__hash_table) * 2 // 3 <= self.__length:
            new_hash_table = [None] * len(self.__hash_table) * 2
            for cell in self.__hash_table:
                if cell is not None and cell != "__TOMBSTONE":
                    new_cell_key_index = cell[1] % len(new_hash_table)
                    Dictionary.table_setter_collision_checker(
                        new_hash_table, new_cell_key_index, cell
                    )
            self.__hash_table = new_hash_table
        key_index = key_hash % len(self.__hash_table)
        is_existing_key = Dictionary.table_setter_collision_checker(
            self.__hash_table, key_index, (key, key_hash, value)
        )
        if is_existing_key:
            self.__length -= 1

    def __getitem__(
        self,
        key: Union[
            int, float, bytes, frozenset, str, bool, complex, tuple, type(None)
        ],
    ) -> Any:
        key_hash = Dictionary.hashing_key(key)
        key_index = key_hash % len(self.__hash_table)
        return Dictionary.value_finder_by_key(
            self.__hash_table, key_index, key
        )[2]

    def __len__(self) -> int:
        return self.__length

    def clear(self) -> None:
        self.__init__()

    def __delitem__(
        self,
        key: Union[
            int, float, bytes, frozenset, str, bool, complex, tuple, type(None)
        ],
    ) -> None:
        key_hash = Dictionary.hashing_key(key)
        key_index = key_hash % len(self.__hash_table)
        if Dictionary.value_finder_by_key(
            self.__hash_table, key_index, key, del_flag=True
        ):
            self.__length -= 1

    def get(
        self,
        key: Union[
            int, float, bytes, frozenset, str, bool, complex, tuple, type(None)
        ],
        default_value: Any = None,
    ) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default_value

    def pop(
        self,
        key: Union[
            int, float, bytes, frozenset, str, bool, complex, tuple, type(None)
        ],
    ) -> Any:
        return_value = self.__getitem__(key)
        self.__delitem__(key)
        return return_value

    def update(self, *args, **kwargs) -> None:
        if args and len(args) == 1:
            arg = args[0]
        else:
            raise ValueError(
                "Dictionary update supports only 1 positional argument"
            )
        if isinstance(arg, Dictionary):
            for other_cell in arg.__hash_table:
                if other_cell is not None:
                    self.__setitem__(other_cell[0], other_cell[2])
        if isinstance(arg, dict):
            for other_key, other_value in arg.items():
                self.__setitem__(other_key, other_value)
        if isinstance(arg, (list, set, tuple, frozenset)):
            nested_all_iterable = False
            for nested in arg:
                if isinstance(nested, (list, set, tuple, frozenset)):
                    nested_all_iterable = True
                else:
                    nested_all_iterable = False
                    break
            if nested_all_iterable and all(
                [len(nested) == 2 for nested in arg]
            ):
                for nested in arg:
                    self.__setitem__(nested[0], nested[1])
            elif len(arg) == 2:
                self.__setitem__(arg[0], arg[1])
            else:
                raise ValueError(
                    "Collection must have 2 elements to be included \
                    into Dictionary or nested collections with 2 items"
                )
        if kwargs:
            for kwargs_key, kwargs_value in kwargs.items():
                self.__setitem__(kwargs_key, kwargs_value)

    def __iter__(self) -> Dictionary:
        self.__index = 0
        return self

    def __next__(self) -> Any:
        while self.__index < len(self.__hash_table):
            result = self.__hash_table[self.__index]
            self.__index += 1
            if result is not None and result != "__TOMBSTONE":
                return result[0]
        raise StopIteration
