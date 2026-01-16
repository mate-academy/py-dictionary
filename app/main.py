from __future__ import annotations
from typing import TypeVar, Any, Mapping
from dataclasses import dataclass, field


_TK = TypeVar("_TK")
_TV = TypeVar("_TV")


@dataclass
class Node:
    key: _TK
    hash_key: int = field(init=False, repr=False)
    value: _TV

    def __post_init__(self) -> None:
        self.hash_key = hash(self.key)


class DictionaryKeys:

    def __init__(self, dictionary: Dictionary[_TK, _TV], /) -> None:
        self._keys = tuple(
            node.key for node in dictionary.__dict__["_hash_table"]
            if node is not None
        )

    def __iter__(self) -> DictionaryKeysIterator:
        return DictionaryKeysIterator(self)


class DictionaryValues:

    def __init__(self, dictionary: Dictionary, /) -> None:
        self._values = tuple(
            node.value for node in dictionary.__dict__["_hash_table"]
            if node is not None
        )

    def __iter__(self) -> DictionaryValuesIterator:
        return DictionaryValuesIterator(self)


class DictionaryItems:

    def __init__(self, dictionary: Dictionary[_TK, _TV], /) -> None:
        self._items = tuple(
            node.value for node in dictionary.__dict__["_hash_table"]
            if node is not None
        )

    def __iter__(self) -> DictionaryItemsIterator:
        return DictionaryItemsIterator(self)


class DictionaryKeysIterator:

    def __init__(self, dictionary_keys: DictionaryKeys, /) -> None:
        self._keys = dictionary_keys.__dict__["_keys"]
        self._index = 0

    def __iter__(self) -> DictionaryKeysIterator:
        return self

    def __next__(self) -> _TK:
        if self._index == len(self._keys):
            raise StopIteration

        key = self._keys[self._index]
        self._index += 1
        return key


class DictionaryValuesIterator:

    def __init__(self, dictionary_values: DictionaryValues, /) -> None:
        self._values = dictionary_values.__dict__["_values"]
        self._index = 0

    def __iter__(self) -> DictionaryValuesIterator:
        return self

    def __next__(self) -> _TV:
        if self._index == len(self._values):
            raise StopIteration

        value = self._values[self._index]
        self._index += 1
        return value


class DictionaryItemsIterator:

    def __init__(self, dictionary_items: DictionaryItems, /) -> None:
        self._items = dictionary_items.__dict__["_items"]
        self._index = 0

    def __iter__(self) -> DictionaryItemsIterator:
        return self

    def __next__(self) -> tuple[_TK, _TV]:
        if self._index == len(self._items):
            raise StopIteration

        key, value = self._items[self._index]
        self._index += 1
        return key, value


class Dictionary(Mapping):

    def __init__(self) -> None:
        self._hash_table: list[None | Node] = [None] * 8
        self._length = 0

    def __str__(self) -> str:
        return (
            "Dictionary({"
            + ", ".join(
                f"{repr(node.key)}: {repr(node.value)}"
                for node in self._hash_table if node is not None
            ) + "})"
        )

    def __iter__(self) -> DictionaryKeysIterator:
        return iter(self.keys())

    def __len__(self) -> int:
        return self._length

    def __getitem__(self, key: _TK, /) -> _TV:
        return self._manage_hash_table(key, get_item=True)

    def __setitem__(self, key: _TK, value: _TV, /) -> None:
        self._manage_hash_table(key, value, set_item=True)

    def __delitem__(self, key: _TK, /) -> None:
        self._manage_hash_table(key, delete_item=True)

    def _get_item_by(self, index: int, /) -> _TV:
        return self._hash_table[index].value

    def _set_item_by(
        self,
        index: int,
        key: _TK,
        value: _TV,
        /,
        *,
        key_exist: bool = False
    ) -> None:
        if key_exist:
            self._hash_table[index].value = value
        else:
            self._hash_table[index] = Node(key, value)
            self._length += 1

    def _delete_item_by(self, index: int, /) -> None:
        self._hash_table[index] = None
        self._length -= 1

    def _manage_hash_table(
        self,
        key: _TK,
        value: _TV | None = None,
        /,
        *,
        get_item: bool = False,
        set_item: bool = False,
        delete_item: bool = False,
    ) -> _TV | None:
        hash_key = hash(key)
        index = hash_key % len(self._hash_table)

        if self._key_by_index_is_found(index, key):
            if get_item:
                return self._get_item_by(index)
            elif set_item:
                self._set_item_by(index, key, value, key_exist=True)
            elif delete_item:
                self._delete_item_by(index)
        else:
            index2, index_none = index + 1, None

            while index2 != index:
                if index2 >= len(self._hash_table):
                    index2 = 0

                if (
                    self._hash_table[index2] is None
                    and index_none is None
                    and set_item
                ):
                    index_none = index2

                if self._key_by_index_is_found(index2, key):
                    if get_item:
                        return self._get_item_by(index2)
                    elif set_item:
                        self._set_item_by(index2, key, value, key_exist=True)
                    elif delete_item:
                        self._delete_item_by(index2)

                    break

                if index2 != index:
                    index2 += 1
            else:
                if get_item or delete_item:
                    raise KeyError(f"Key '{key}' is not in dictionary")
                else:
                    self._set_item_by(index_none, key, value)

                    if self._reached_threshold():
                        self._resize_hash_table()

    def _key_by_index_is_found(self, index: int, key: _TK, /) -> bool:
        return (
            self._hash_table[index] is not None
            and self._hash_table[index].key == key
        )

    def _reached_threshold(self) -> bool:
        return self._length == int(len(self._hash_table) * (2 / 3))

    def _resize_hash_table(self) -> None:
        new_hash_table: list[Node | None] = (
            [None] * (len(self._hash_table) * 2)
        )
        count = 0
        for index in range(len(self._hash_table)):
            if count == self._length:
                break

            if self._hash_table[index] is not None:
                count += 1
                hash_key = self._hash_table[index].hash_key
                index2 = hash_key % len(new_hash_table)
                if new_hash_table[index2] is None:
                    new_hash_table[index2] = Node(
                        self._hash_table[index].key,
                        self._hash_table[index].value
                    )
                else:
                    index3 = index2 + 1
                    while index3 != index2:
                        if index3 >= len(new_hash_table):
                            index3 = 0

                        if new_hash_table[index3] is None:
                            new_hash_table[index3] = Node(
                                self._hash_table[index].key,
                                self._hash_table[index].value
                            )
                            break

                        if index3 != index2:
                            index3 += 1

        self._hash_table = new_hash_table

    def get(self, key: _TK, default: Any | None = None, /) -> _TV:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: _TK, /) -> _TV:
        value = self[key]
        del self[key]
        return value

    def clear(self) -> None:
        begin_index, end_index = 0, len(self._hash_table) - 1

        while begin_index != end_index and self._length:
            if self._hash_table[begin_index] is not None:
                self._hash_table[begin_index] = None
                self._length -= 1

            begin_index += 1

            if self._hash_table[end_index] is not None:
                self._hash_table[end_index] = None
                self._length -= 1

            end_index -= 1

    def update(self, mapping_object: Mapping, **kwargs) -> None:
        for key, value in mapping_object.items():
            self[key] = value

        for key, value in kwargs.items():
            self[key] = value

    def keys(self) -> DictionaryKeys[_TK]:
        return DictionaryKeys(self)

    def values(self) -> DictionaryValues[_TV]:
        return DictionaryValues(self)


if __name__ == "__main__":
    d = Dictionary()
    d["name"] = "Bogdan"
    d["age"] = 20
    d["birth_year"] = 2004
    print(d)

    del d["birth_year"]

    print(d)
