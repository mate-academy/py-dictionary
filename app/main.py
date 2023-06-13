from typing import Any, Hashable, NamedTuple


DELETED = object()


class Pair(NamedTuple):
    key: Any
    value: Any

    def __str__(self) -> str:
        return f"{self.key!r}: {self.value!r}"

    def __repr__(self) -> str:
        return f"({self.key!r}, {self.value!r})"


class Dictionary:
    @classmethod
    def from_dict(cls, dictionary: object, capacity: int = None) -> Any:
        hash_table = cls(capacity or len(dictionary))
        for key, value in dictionary.items():
            hash_table[key] = value
        return hash_table

    def __init__(self,
                 capacity: int = 8,
                 load_factor_threshold: float = 0.6) -> None:
        if capacity < 1:
            raise ValueError("Capacity must be a positive")
        if not (0 < load_factor_threshold <= 1):
            raise ValueError("Load factor must be a number between (0, 1]")
        self._slots = capacity * [None]
        self._load_factor_threshold = load_factor_threshold

    def __len__(self) -> int:
        return len(self.pairs)

    def __iter__(self) -> Any:
        yield from self.keys

    def __delitem__(self, key: Hashable) -> None:
        for index, pair in self._probe(key):
            if pair is None:
                raise KeyError(key)
            if pair is DELETED:
                continue
            if pair.key == key:
                self._slots[index] = DELETED
                break

    def __setitem__(self, key: Hashable, value: Any) -> None:
        """all the available slots in the hash table,
               starting from the calculated by hash index"""
        if self.load_factor >= self._load_factor_threshold:
            self._resize_and_rehash()
        for index, pair in self._probe(key):
            if pair is DELETED:
                continue
            if pair is None or pair.key == key:
                self._slots[index] = Pair(key, value)
                break

    def __getitem__(self, key: Hashable) -> Any:
        """calculate the index of an element based
        on the hash code of the provided key
         and return whatever sits under that index. """
        for _, pair in self._probe(key):
            if pair is None:
                raise KeyError(key)
            if pair is DELETED:
                continue
            if pair.key == key:
                return pair.value
        raise KeyError(key)

    def __contains__(self, key: Hashable) -> bool:
        try:
            self[key]
        except KeyError:
            return False
        return True

    def __eq__(self, other: object) -> bool:
        if self is other:
            return True
        if type(self) is not type(other):
            return False
        return set(self.pairs) == set(other.pairs)

    def __str__(self) -> str:
        pairs = []
        for key, value in self.pairs:
            pairs.append(f"{key!r}: {value!r}")
        return "{" + ", ".join(pairs) + "}"

    def __repr__(self) -> str:
        cls = self.__class__.__name__
        return f"{cls}.from_dict({str(self)})"

    def copy(self) -> object:
        cls = self.__class__
        return cls.from_dict(dict(self.pairs), self.capacity)

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    @property
    def pairs(self) -> list:
        return [pair for pair in self._slots if pair not in (None, DELETED)]

    @property
    def keys(self) -> set:
        return {pair.key for pair in self.pairs}

    @property
    def values(self) -> list:
        return [pair.value for pair in self.pairs]

    @property
    def capacity(self) -> int:
        return len(self._slots)

    @property
    def load_factor(self) -> float:
        occupied_or_deleted = [slot for slot in self._slots if slot]
        return len(occupied_or_deleted) / self.capacity

    def _index(self, key: Hashable) -> int:
        """Turn an arbitrary key into a numeric hash value
         and use the % operator to constrain the resulting index
         within the available address space."""
        return hash(key) % self.capacity

    def clear(self) -> None:
        self._load_factor_threshold = 0.6
        self._slots = 8 * [None]

    def _probe(self, key: Hashable) -> Any:
        """ linear probing will be used in create/reading
         operations in the hash table.
        At each step, return the current index
        and the associated pair"""

        index = self._index(key)
        for _ in range(self.capacity):
            """At each step, return
             the current index and the associated pair"""
            yield index, self._slots[index]
            index = (index + 1) % self.capacity

    def _resize_and_rehash(self) -> None:
        copy = Dictionary(capacity=self.capacity * 2)
        for key, value in self.pairs:
            copy[key] = value
        self._slots = copy._slots
