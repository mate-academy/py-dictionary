from __future__ import annotations


class DictionaryIterator:
    def __init__(self, dictionary_: Dictionary) -> None:
        self.dictionary = dictionary_
        self.current_size = self.dictionary.length
        self.current_index = 0

    def __iter__(self) -> DictionaryIterator:
        return self

    def __next__(self) -> any:
        if self.dictionary.length != self.current_size:
            raise Exception("dictionary changed size during iteration")

        hash_table = self.dictionary.hash_table

        while (
                self.current_index < self.dictionary.capacity
                and (
                    not hash_table[self.current_index]
                    or hash_table[self.current_index]["deleted"]
                )
        ):
            self.current_index += 1

        if (
                self.current_index == self.dictionary.capacity
                or not hash_table[self.current_index]
        ):
            raise StopIteration

        key = hash_table[self.current_index]["key"]
        self.current_index += 1

        return key


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.length = 0
        self.hash_table = [None] * 8
        self.load_factor = 2 / 3

    def __iter__(self) -> DictionaryIterator:
        return DictionaryIterator(self)

    def __setitem__(self, key: any, value: any) -> None:
        key_hash = hash(key)
        hash_index = key_hash % self.capacity
        index = hash_index
        index_to_insert = index

        if self.hash_table[index] and self.hash_table[index]["key"] != key:
            index = (index + 1) % self.capacity
            while (
                    not self.hash_table[index]
                    or (
                        index != hash_index
                        and self.hash_table[index]["key"] != key
                    )
            ):
                if (
                        not self.hash_table[index]
                        or self.hash_table[index]["deleted"]
                ) and index_to_insert == hash_index:
                    index_to_insert = index
                index = (index + 1) % self.capacity

            if index == hash_index:
                index = index_to_insert

        if not self.hash_table[index] or self.hash_table[index]["deleted"]:
            self.length += 1

        self.hash_table[index] = {
            "key": key,
            "hash": key_hash,
            "value": value,
            "deleted": False,
        }

        if self.length > self.capacity * self.load_factor:
            self.__resize()

    def __getitem__(self, key: any) -> any:
        key_hash = hash(key)
        index = key_hash % self.capacity

        while (
                self.hash_table[index]
                and self.hash_table[index]["key"] != key
        ):
            index = (index + 1) % self.capacity

        if not self.hash_table[index] or self.hash_table[index]["deleted"]:
            raise KeyError(key)

        return self.hash_table[index]["value"]

    def __len__(self) -> int:
        return self.length

    def __delitem__(self, key: any) -> None:
        key_hash = hash(key)
        hash_index = key_hash % self.capacity
        index = hash_index

        while (
                not self.hash_table[index]
                or self.hash_table[index]["key"] != key
        ):
            index = (index + 1) % self.capacity

            if index == hash_index:
                raise KeyError(key)

        self.hash_table[index].update(
            {"deleted": True}
        )

        self.length -= 1

    def __resize(self) -> None:
        self.capacity *= 2
        old_hash_table = self.hash_table
        self.length = 0
        self.hash_table = [None] * self.capacity

        for hash_table_value in old_hash_table:
            if hash_table_value:
                self.__setitem__(
                    hash_table_value["key"],
                    hash_table_value["value"]
                )

    def clear(self) -> None:
        self.capacity = 8
        self.hash_table = [None] * self.capacity
        self.length = 0

    def get(self, key: any, default_value: any = None) -> any:
        try:
            return self[key]
        except KeyError:
            return default_value

    def pop(self, key: any, *args: any) -> any:
        if len(args) > 1:
            raise TypeError(
                f"pop expected at most 2 arguments, got {len(args) + 1}"
            )

        try:
            value = self[key]
            del self[key]
        except KeyError:
            if len(args) == 1:
                return args[0]
            raise

        return value

    def update(self, *args, **kwargs) -> None:
        if args and len(args) != 1:
            raise TypeError(
                "update expected at most 1 positional "
                "argument, got 2"
            )

        if args:
            if hasattr(args[0], "keys"):
                keys = args[0].keys()
                for key in keys:
                    self[key] = args[0][key]
            else:
                for index, item in enumerate(args[0]):
                    if len(item) != 2:
                        raise ValueError(
                            f"dictionary update sequence element #{index} "
                            f"has length {len(item)} but 2 is required"
                        )
                    self[item[0]] = item[1]

        if kwargs:
            for key, value in kwargs.items():
                self[key] = value
