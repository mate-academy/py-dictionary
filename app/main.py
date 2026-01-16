from typing import Any, Iterable, Tuple

from app.node import Node


class Dictionary:
    def __init__(self) -> None:
        """Initialize the dictionary with
        default capacity and internal storage."""
        self.capacity = 8
        self.size = 0
        self.koff = 2 / 3
        self.threshold = round(self.capacity * self.koff)
        self.bucket: list[Node | None] = [None] * self.capacity

    def __hash_index(self, key: Any) -> int:
        """
    Compute the hash index for a given key based on the current table size.
    Args:
        key: The key to be hashed.
    Returns:
        The index position within the current hash table capacity.
    """
        return hash(key) % self.capacity

    def __verify_slot(self, idx: int, key: Any, option: str) -> bool:
        """
    Check the status of a slot in the hash table depending on the operation.
    Args:
        idx: The current index in the hash table.
        key: The key being searched or inserted.
        option: The verification mode.
            - "new": Checks if the slot is occupied by a different key.
            - "empty": Checks if the slot is free or a tombstone.
            - "current": Checks if the slot contains the target key.
    Returns:
        True if the condition for the given
        option is satisfied, otherwise False.
    Raises:
        ValueError: If an invalid option is provided.
    """
        entry = self.bucket[idx]
        match option:
            case "new":
                return (entry is not None
                        and entry.key != key)
            case "empty":
                return entry is None
            case "current":
                return entry.key == key
            case _:
                raise ValueError(f"Invalid slot option: {option}")

    def __setitem__(self, key: Any, value: Any) -> None:
        """
    Insert or update a key-value pair in the dictionary.
    Args:
        key: The key to insert or update.
        value: The value to associate with the key.
    Raises:
        RuntimeError: If resizing or insertion fails unexpectedly.
    """
        idx = self.__hash_index(key)

        while self.__verify_slot(idx, key, "new"):
            idx = (idx + 1) % self.capacity

        if self.__verify_slot(idx, key, "empty"):
            self.size += 1

        self.bucket[idx] = Node(key, value)

        if self.size > self.threshold:
            self.__resize()

    def __getitem__(self, key: Any) -> Any:
        """
    Retrieve the value associated with a given key.
    Args:
        key: The key to look up in the dictionary.
    Returns:
        The value associated with the key.
    Raises:
        KeyError: If the key does not exist in the dictionary.
    """
        idx = self.__hash_index(key)

        while self.bucket[idx] is not None:
            entry = self.bucket[idx]
            if self.__verify_slot(idx, key, "current"):
                return entry.value
            idx = (idx + 1) % self.capacity

        raise KeyError(key)

    def __delitem__(self, key: Any) -> None:
        """
    Remove a key-value pair from the dictionary
    and mark its slot as a tombstone.
    Args:
        key: The key to remove.
    Raises:
        KeyError: If the key is not found.
    """
        idx = self.__hash_index(key)

        while self.bucket[idx] is not None:
            if self.__verify_slot(idx, key, "current"):
                self.bucket[idx] = [None]
                self.size -= 1
                return
            idx = (idx + 1) % self.capacity

        raise KeyError(key)

    def __len__(self) -> int:
        """Return the number of active key-value pairs."""
        return self.size

    def __iter__(self) -> Any:
        """Iterate over keys."""
        for entry in self.bucket:
            if isinstance(entry, Node):
                yield entry.key

    def items(self) -> Any:
        """Iterate over (key, value) pairs."""
        for entry in self.bucket:
            if isinstance(entry, Node):
                yield (entry.key, entry.value)

    def values(self) -> Any:
        """Iterate over all values."""
        for entry in self.bucket:
            if isinstance(entry, Node):
                yield entry.value

    def __resize(self) -> None:
        """Double capacity and rehash all nodes."""
        old_bucket = self.bucket

        self.capacity *= 2
        self.bucket = [None] * self.capacity
        self.size = 0
        self.threshold = round(self.capacity * (2 / 3))

        for entry in old_bucket:
            if isinstance(entry, Node):
                self.__setitem__(entry.key, entry.value)

    def clear(self) -> None:
        """Remove all entries."""
        self.__init__()

    def get(self, key: Any, default: Any = None) -> Any:
        """
    Retrieve the value for a key if it exists,
    otherwise return a default value.
    Args:
        key: The key to look up.
        default: The value to return if the key is not found. Defaults to None.
    Returns:
        The value associated with the key, or the provided default.
    """
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Any) -> Any:
        """
    Remove and return a key-value pair by index or the last inserted element.
    Args:
        key: The key of the key-value pair to remove.
               If None return None
    Returns:
        A tuple containing (key, value) of the removed element.
    Raises:
        KeyError: If the dictionary is empty.
    """
        if self.size == 0:
            raise KeyError("Dictionary is empty")

        if key:
            value = self[key]
            self.__delitem__(key)
            return key, value
        else:
            return None

    def update(self,
               updates: Iterable[Tuple[Any, Any]] | dict | tuple) -> None:
        """
    Update the dictionary with key-value pairs
    from another dictionary or iterable.
    Args:
        updates: A dictionary, an iterable of (key, value) pairs,
                 or a single (key, value) tuple.
    Raises:
        TypeError: If updates is not a valid iterable or mapping type.
    """
        if isinstance(updates, dict):
            updates = updates.items()
        if (isinstance(updates, tuple)
                and len(updates) == 2
                and not isinstance(updates[0], tuple)):
            updates = [updates]
        for key, value in updates:
            self[key] = value
