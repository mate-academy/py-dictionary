"""
A custom implementation of a dictionary using a hash table.

This module provides a from-scratch implementation of a dictionary-like
data structure called ``Dictionary``. It uses open addressing with a
key-dependent linear probing sequence for collision resolution.
"""
from __future__ import annotations
from typing import NamedTuple, Hashable, Iterator


Pair = tuple[Hashable, object]
DictCells = "list[Cell | type(_DELETED) | None]"


class Cell(NamedTuple):
    """
    Represents a single cell in the hash table.

    :param key: The key of the item.
    :param hashed: The pre-computed hash of the key.
    :param value: The value associated with the key.
    """
    key: Hashable
    hashed: int
    value: object


class Dictionary:
    """
    A custom dictionary implementation using a hash table.

    This class mimics the behavior of Python's built-in ``dict``,
    including support for standard dictionary operations like setting,
    getting, and deleting items. It automatically handles resizing and
    rehashing to maintain performance.

    :Class Attributes:
        * ``_DELETED``: A sentinel object used to mark slots from which
          items have been deleted. This helps in distinguishing between
          empty slots and deleted slots during probing.
        * ``size_threshold`` (float): The load factor at which the hash
          table will be resized (rehashed) to a larger capacity. When
          the ratio of stored items to capacity exceeds this value, a
          rehash occurs.
        * ``deleted_threshold`` (float): The threshold for the proportion
          of deleted slots to the total capacity. If the number of
          deleted slots exceeds this proportion, a rehash is triggered
          to reclaim space and improve lookup performance.
        * ``init_capacity_power`` (int): The power of 2 for the initial
          capacity of the hash table. The initial capacity will be
          ``2 ** init_capacity_power``.
    """
    _DELETED = object()
    size_threshold: float = 2 / 3
    deleted_threshold: float = 1 / 3
    init_capacity_power: int = 3

    def __init__(
            self,
            *args: Pair,
    ) -> None:
        """
        Initializes the Dictionary.

        :param args: An optional sequence of key-value pairs (tuples) to
                     populate the dictionary with.
        """
        self.__capacity = 2 ** self.init_capacity_power
        self.__length = 0
        self.__deleted = 0
        self.__cells: DictCells = [None] * self.__capacity
        if args:
            for data in args:
                self.__setitem__(*data)

    def __probe(
            self,
            key: Hashable,
            hashed: int
    ) -> tuple[int, Cell | None]:
        """
        Internal method to find the index for a key in the hash table.

        This method probes the hash table to find the correct index for a
        given key. It follows a linear probing sequence with a step size
        derived from the key's hash.

        It returns one of the following:
        - If the key is found, it returns the index and the ``Cell``
          object.
        - If the key is not found, it returns the index of the first
          available (empty or deleted) slot and ``None``.

        :param key: The key to probe for.
        :param hashed: The pre-computed hash of the key.
        :returns: A tuple containing the found index and an optional
                  ``Cell``.
        """
        index = hashed & (self.__capacity - 1)
        step = (hashed >> 16) | 1
        del_cell_index = None
        while True:
            cell = self.__cells[index]

            if cell is None:
                return (del_cell_index or index), None

            if del_cell_index is None and cell is self._DELETED:
                del_cell_index = index

            if (
                isinstance(cell, Cell)
                and cell.hashed == hashed
                and cell.key == key
            ):
                return index, cell

            index = (index + step) & (self.__capacity - 1)

    def __rehash(self) -> None:
        """
        Internal method to resize and rebuild the hash table.

        This is triggered when the dictionary exceeds its size or deleted
        cell thresholds. It creates a new, larger table and re-inserts
        all existing items, discarding deleted slots.
        """
        stored_cells: DictCells = [
            cell
            for cell in self.__cells
            if cell is not None and cell is not self._DELETED
        ]
        self.__cells = [None] * self.__capacity
        self.__length = 0
        self.__deleted = 0
        for cell in stored_cells:
            index, _ = self.__probe(cell.key, cell.hashed)
            self.__cells[index] = cell
            self.__length += 1

    def __setitem__(self, key: Hashable, value: object) -> None:
        """
        Sets the value for a given key, like ``d[key] = value``.

        If the key already exists, its value is updated. If it's a new
        key, a new item is added. Triggers a rehash if the dictionary
        becomes too full.

        :param key: The key of the item to set.
        :param value: The value to associate with the key.
        """
        hashed = hash(key)
        index, stored_cell = self.__probe(key, hashed)

        if isinstance(stored_cell, Cell) and stored_cell.value == value:
            return

        self.__cells[index] = Cell(key, hashed, value)

        if stored_cell is None:
            self.__length += 1

            if self.__length / self.__capacity >= self.size_threshold:
                self.__capacity *= 2
                self.__rehash()
                return

    def __getitem__(self, key: Hashable) -> object:
        """
        Retrieves the value for a given key, like ``d[key]``.

        :param key: The key of the item to retrieve.
        :returns: The value associated with the key.
        :raises KeyError: If the key is not found in the dictionary.
        """
        _, stored_cell = self.__probe(key, hash(key))
        if stored_cell is None:
            raise KeyError(key)
        return stored_cell.value

    def __delitem__(self, key: Hashable) -> None:
        """
        Deletes an item from the dictionary, like ``del d[key]``.

        The item's slot is marked as deleted. Triggers a rehash if the
        number of deleted slots becomes too high.

        :param key: The key of the item to delete.
        :raises KeyError: If the key is not found in the dictionary.
        """
        index, stored_cell = self.__probe(key, hash(key))

        if stored_cell is None:
            raise KeyError(key)

        self.__cells[index] = self._DELETED
        self.__deleted += 1
        self.__length -= 1

        if self.__deleted >= self.__capacity * self.deleted_threshold:
            self.__rehash()

    def __len__(self) -> int:
        """
        Returns the number of items in the dictionary.

        :returns: The total number of items.
        """
        return self.__length

    def __iter__(self) -> Iterator:
        """
        Returns an iterator over the keys of the dictionary.

        :returns: An iterator yielding the keys.
        """
        for cell in self.__cells:
            if cell is not None and cell is not self._DELETED:
                yield cell.key

    def clear(self) -> None:
        """Removes all items from the dictionary."""
        self.__length = 0
        self.__deleted = 0
        self.__cells = [None] * self.__capacity

    def get(
            self,
            key: Hashable,
            default: object | None = None
    ) -> object | None:
        """
        Gets the value for a key, returning a default value if not found.

        :param key: The key of the item to retrieve.
        :param default: The value to return if the key is not found.
        :returns: The value of the item or the default value.
        """
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def pop(
            self,
            key: Hashable,
            default: object | None = None
    ) -> object | None:
        """
        Removes an item and returns its value.

        If the key is not found, the default value is returned.

        :param key: The key of the item to remove.
        :param default: The value to return if the key is not found.
        :returns: The value of the removed item or the default value.
        """
        try:
            value = self.__getitem__(key)
        except KeyError:
            return default
        else:
            self.__delitem__(key)
            return value

    def update(self, *args: Pair | Dictionary) -> None:
        """
        Updates the dictionary with items from another source.

        The source can be another ``Dictionary`` instance or a sequence of
        key-value pairs.

        :param args: The source(s) to update from.
        """
        for data in args:
            if isinstance(data, Dictionary):
                for key in data:
                    self.__setitem__(key, data[key])
                continue

            self.__setitem__(*data)
