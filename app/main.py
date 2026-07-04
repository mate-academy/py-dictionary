"""Simple custom dictionary implementation using open hashing."""

from __future__ import annotations


class Dictionary():
    """
    Dictionary implementation with basic hashing and resizing.
    """

    def __init__(self) -> None:
        self.d_length = 0
        self.hash_size = 8
        self.hash_table = [[] for _ in range(self.hash_size)]

    def __len__(self) -> int:
        return self.d_length

    def __setitem__(
            self,
            key: str | int | float | bool,
            value: str | int | float | bool) -> None:
        hash_key = hash(key)

        hash_index = hash_key % self.hash_size

        for _item in self.hash_table[hash_index]:
            if _item[0] == key:
                _item[2] = value
                return

        self.hash_table[hash_index].append([key, hash_key, value])

        self.d_length += 1

        if self.d_length / self.hash_size > 0.7:
            self._resize()

    def __getitem__(self,
                    key: str | int | float | bool
                    ) -> str | int | float | bool:
        hash_key = hash(key)
        hash_index = hash_key % self.hash_size

        for item in self.hash_table[hash_index]:
            if item[0] == key:
                return item[2]

        raise KeyError(f"Key '{key}' not found in the dictionary.")

    def __delitem__(self,
                    key: str | int | float | bool) -> None:
        hash_key = hash(key)
        hash_index = hash_key % self.hash_size

        for _item in self.hash_table[hash_index]:
            if _item[0] == key:
                self.hash_table[hash_index].remove(_item)
                self.d_length -= 1
                return

        raise KeyError(f"Key '{key}' not found in the dictionary.")

    def __iter__(self) -> iter[str | int | float | bool]:
        for items in self.hash_table:
            if items:
                for key in items:
                    yield key[0]

    def _resize(self) -> None:
        self.hash_size *= 2
        new_hash_table = [[] for _ in range(self.hash_size)]

        for items in self.hash_table:
            if items:
                for _item in items:
                    key, hash_key, value = _item
                    hash_index = hash_key % self.hash_size
                    new_hash_table[hash_index].append([key, hash_key, value])
        self.hash_table = new_hash_table

    def clear(self) -> None:
        """
        Remove all items from the dictionary and reset internal storage.
        """
        self.d_length = 0
        self.hash_size = 8
        self.hash_table = [[] for _ in range(self.hash_size)]

    def get(self,
            key: str | int | float | bool,
            default: str | int | float | bool = None
            ) -> str | int | float | bool | None:
        """
        Return value for key if present, otherwise default.

        Args:
            key: The key to look up.
            default: Value to return if key is not found.

        Returns:
            The value associated with key or default if not present.
        """

        hash_key = hash(key)
        hash_index = hash_key % self.hash_size

        for item in self.hash_table[hash_index]:
            if item[0] == key:
                return item[2]
        return default

    def pop(self,
            key: str | int | float | bool,
            default: str | int | float | bool = None
            ) -> str | int | float | bool | None:
        """Remove specified key and return the corresponding value.

        If key is not found, return default if provided,
            otherwise raise KeyError.
        """
        hash_key = hash(key)
        hash_index = hash_key % self.hash_size

        for _item in self.hash_table[hash_index]:
            if _item[0] == key:
                value = _item[2]
                self.hash_table[hash_index].remove(_item)
                self.d_length -= 1
                return value

        if default is not None:
            return default
        raise KeyError(f"Key '{key}' not found in the dictionary.")

    def update(self,
               other: dict | Dictionary) -> None:
        """Update the dictionary with items from another mapping.

        Accepts either another Dictionary instance or a built-in dict.
        Existing keys will be overwritten with values from the provided
        mapping.
        """
        if isinstance(other, Dictionary):
            for items in other.hash_table:
                if items:
                    for _item in items:
                        key = _item[0]
                        value = _item[2]
                        self[key] = value
        elif isinstance(other, dict):
            for key, value in other.items():
                self[key] = value
        else:
            raise TypeError("Argument must be a Dictionary or a dict.")
