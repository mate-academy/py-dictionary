from typing import Hashable, Any


class Dictionary:

    _INITIAL_CAPACITY = 8
    _LOAD_FACTOR = 2 / 3

    def __init__(self) -> None:
        self.dict_length = 0
        self.hash_table_length = Dictionary._INITIAL_CAPACITY
        self.hash_table: list = [None] * self.hash_table_length

    def __len__(self) -> int:
        return self.dict_length

    def __getitem__(self, key: Hashable) -> Any:
        # try get hash:
        try:
            hash_ = Dictionary._get_hash(key)
        except KeyError(f"Cannot add an item with a `{type(key)}`-type key"):
            return

        # from the key and its hash, we get the index of the current or the
        # closest "equal" slot:
        index = hash_ % self.hash_table_length
        search_iteration = 0
        while not self.hash_table[index] or key != self.hash_table[index][0]:
            index = (index + 1) % self.hash_table_length
            search_iteration += 1
            if search_iteration >= self.hash_table_length:
                raise KeyError(f"Cannot get value: key {key} not in {self}")

        # and we return the value by that index:
        return self.hash_table[index][2]

    def __setitem__(self, key: Hashable, value: Any) -> None:
        # we try get hash:
        try:
            hash_ = Dictionary._get_hash(key)
        except KeyError(f"Cannot add an item with a `{type(key)}`-type key"):
            return

        # having validated the key we now conditionally increase the capacity:
        if self.dict_length / self.hash_table_length >= (
                Dictionary._LOAD_FACTOR):
            self._increase_capacity()

        # finally, we actually set the item:
        new_item_added = self._setitem(self.hash_table, (key, hash_, value))

        # and we conditionally increment the actual length of the dict:
        if new_item_added:
            self.dict_length += 1

    def clear(self) -> None:
        for index in range(self.hash_table_length):
            self.hash_table[index] = None

    @staticmethod
    def _get_hash(obj: Hashable) -> int:
        try:
            return hash(obj)
        except TypeError(f"Key `{obj}` of type `{type(obj)}` is not hashable"):
            raise

    def _increase_capacity(self) -> None:
        self.hash_table_length *= 2
        new_hash_table = [None] * self.hash_table_length
        for dict_item in self.hash_table:
            if dict_item:
                self._setitem(new_hash_table, dict_item)
        self.hash_table = new_hash_table

    def _setitem(self, hash_table: list, dict_item: tuple) -> bool:
        # we check whether the same key exists already in the hash table:
        for index, ht_item in enumerate(hash_table):
            if ht_item and ht_item[0] == dict_item[0]:  # key equality
                hash_table[index] = dict_item
                return False  # because of NO NEW ITEM was added to dictionary

        # the key is new, so we put the `dict_item` tuple where appropriate:
        index = dict_item[1] % self.hash_table_length  # hash % length
        while hash_table[index]:
            index = (index + 1) % self.hash_table_length

        hash_table[index] = dict_item
        return True  # because A NEW ITEM was added to the dictionary
