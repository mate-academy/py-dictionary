from fractions import Fraction
from typing import Any, Generator, Hashable, Iterable, Optional


class Dictionary:
    class __Node:
        def __init__(
                self,
                key: Optional[Hashable] = None,
                value: Optional[Any] = None,
                key_hash: Optional[int] = None
        ) -> None:
            self.key = key
            self.value = value
            self.key_hash = key_hash
            self.deleted = False

    def __init__(
            self,
            initial_data: Optional[Iterable[tuple[Hashable, Any]]] = None,
            **kwargs
    ) -> None:
        self.__capacity = 8
        self.__size = 0
        self.__threshold = int(Fraction(2, 3) * self.__capacity)
        self.__table = [Dictionary.__Node()] * self.__capacity

        if initial_data:
            self.update(initial_data)
        if kwargs:
            self.update(**kwargs)

    def __repr__(self) -> str:
        items = ", ".join(f"{key}: {value}" for key, value in self.items())
        return f"{{{items}}}"

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self.__calculate_index(key)

        if self.__table[index].key is None:
            if self.__size + 1 > self.__threshold:
                self.__resize(key, value)
                return
            self.__size += 1

        self.__table[index] = Dictionary.__Node(key, value, hash(key))

    def __getitem__(self, key: Hashable) -> Any:
        index = self.__calculate_index(key)

        if self.__table[index].key is None:
            raise KeyError(key)

        return self.__table[index].value

    def __delitem__(self, key: Hashable) -> None:
        index = self.__calculate_index(key)

        if self.__table[index].key is None:
            raise KeyError(key)

        self.__table[index] = Dictionary.__Node()
        self.__table[index].deleted = True
        self.__size -= 1

    def __len__(self) -> int:
        return self.__size

    def __iter__(self) -> Generator:
        return (node.key for node in self.__table if node.key)

    def clear(self) -> None:
        self.__table = [Dictionary.__Node()] * self.__capacity
        self.__size = 0

    def get(self, key: Hashable, value: Optional[Any] = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return value

    def pop(self, key: Hashable, default_value: Optional[Any] = None) -> Any:
        try:
            value_to_return = self[key]
            del self[key]
            return value_to_return
        except KeyError:
            if default_value:
                return default_value
            raise

    def update(
            self,
            data: Optional[Iterable[tuple[Hashable, Any]]] = None,
            **kwargs
    ) -> None:
        if data:
            for key, value in data:
                self[key] = value

        for key, value in kwargs.items():
            self[key] = value

    def items(self) -> list[tuple[Hashable, Any]]:
        return [
            (node.key, node.value)
            for node in self.__table
            if node.key is not None
        ]

    def keys(self) -> list[Hashable]:
        return [
            node.key
            for node in self.__table
            if node.key is not None
        ]

    def values(self) -> list[Any]:
        return [
            node.value
            for node in self.__table
            if node.key is not None
        ]

    def copy(self) -> "Dictionary":
        return Dictionary(self.items())

    def __calculate_index(self, key: Hashable) -> int:
        index = hash(key) % self.__capacity

        while (
            self.__table[index].key is not None
            and self.__table[index].key != key
            or self.__table[index].deleted is True
        ):
            index = (index + 1) % self.__capacity

        return index

    def __resize(self, key: Hashable, value: Any) -> None:
        self.__capacity *= 2
        self.__size = 0
        self.__threshold = int(Fraction(2, 3) * self.__capacity)
        self.__table_before_resize = self.__table
        self.__table = [Dictionary.__Node()] * self.__capacity

        for node in self.__table_before_resize:
            if node.key is not None:
                self[node.key] = node.value

        del self.__table_before_resize

        self[key] = value
