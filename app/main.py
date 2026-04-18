from typing import Any, List, Optional, Tuple
DictNode = Optional[Tuple[Any, int, Any]]


class Dictionary:
    LOAD_FACTOR_THRESHOLD = 2 / 3

    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.table: List[DictNode] = [None] * self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.length >= self.capacity * self.LOAD_FACTOR_THRESHOLD:
            self._resize()

        key_hash = hash(key)
        index = key_hash % self.capacity

        while self.table[index] is not None:
            # If the keys are equal, we update the value
            if self.table[index][0] == key:
                # Store all three pieces of info
                self.table[index] = (key, key_hash, value)
                return
            # Collision! Move to the next slot
            index = (index + 1) % self.capacity

        # Found an empty slot
        self.table[index] = (key, key_hash, value)
        self.length += 1

    def __getitem__(self, key: Any) -> Any:
        key_hash = hash(key)
        index = key_hash % self.capacity
        start_index = index

        # Linear Probing to find the key
        while self.table[index] is not None:
            if self.table[index][0] == key:
                return self.table[index][2]
            index = (index + 1) % self.capacity

            # If we've looped back to start, it's definitely not here
            if index == start_index:
                break

        raise KeyError(f"Key '{key}' not found in Dictionary.")

    def __len__(self) -> int:
        return self.length

    def _resize(self) -> None:
        """Doubles capacity and rehashes all existing items."""
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.length = 0

        for node in old_table:
            if node is not None:
                # Now this will work because there are 3 items to unpack
                key, key_hash, value = node
                self.__setitem__(key, value)
