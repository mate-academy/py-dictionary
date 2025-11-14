from __future__ import annotations
from typing import NamedTuple, Hashable, Iterator


Pair = tuple[Hashable, object]


class Cell(NamedTuple):
    key: Hashable
    hash: int
    value: object


class Dictionary:
    _DELETED = object()

    def __init__(
            self,
            *args: tuple[Hashable, object],
            size_threshold: float = 2 / 3,
            deleted_threshold: float = 1 / 3,
            init_capacity_power: int = 3
    ) -> None:
        self.__threshold = size_threshold
        self.__deleted_threshold = deleted_threshold
        self.__capacity = 2 ** init_capacity_power
        self.__length = 0
        self.__deleted = 0
        self.__cells = [None] * self.__capacity
        if args:
            for pair in args:
                self.__setitem__(*pair)

    def __probe(
            self,
            key: Hashable,
            _hash: int | None = None
    ) -> tuple[int, int, object]:
        if _hash is None:
            _hash = hash(key)
        index = _hash & (self.__capacity - 1)

        deleted_cell_index = None
        step = 1
        while True:
            cell = self.__cells[index]

            if cell is None:
                return (deleted_cell_index or index), _hash, None

            if deleted_cell_index is None and cell is self._DELETED:
                deleted_cell_index = index
            else:
                stored_key, stored_hash, stored_value = cell
                if stored_hash == _hash and stored_key == key:
                    return index, _hash, stored_value

            index = (index + step ** 2) & (self.__capacity - 1)
            step += 1

    def __resize(
            self,
            *new_cells: tuple[Hashable, int, object],
            capacity_multiplier_power: int = 1
    ) -> None:
        stored_data = [
            cell
            for cell in self.__cells
            if cell is not None and cell is not self._DELETED
        ]
        if new_cells :
            stored_data += [*new_cells]

        self.__capacity *= 2 ** capacity_multiplier_power
        self.__cells = [None] * self.__capacity
        self.__length = 0
        self.__deleted = 0
        for stored_key, stored_hash, stored_value in stored_data:
            self.__setitem__(stored_key, stored_value, stored_hash)

    def __getitem__(self, key: Hashable) -> object:
        _, _, stored_value = self.__probe(key)
        if stored_value is None:
            raise KeyError(key)
        return stored_value

    def __setitem__(
            self,
            key: Hashable,
            value: object,
            _hash: int | None = None
    ) -> None:
        index, _hash, stored_value = self.__probe(key, _hash)

        if stored_value is None:
            if (self.__length + 1) / self.__capacity >= self.__threshold:
                self.__resize((key, _hash, value))
                return

            self.__length += 1
        self.__cells[index] = (key, _hash, value)

    def __len__(self) -> int:

        return self.__length

    def __delitem__(self, key: Hashable) -> None:
        index, _, stored_value = self.__probe(key)

        if stored_value is None:
            raise KeyError(key)

        self.__cells[index] = self._DELETED
        self.__deleted += 1
        self.__length -= 1

        if self.__deleted >= self.__capacity * self.__deleted_threshold:
            self.__resize(capacity_multiplier_power=0)

    def __iter__(self) -> Iterator:
        for cell in self.__cells:
            if cell is not None and cell is not self._DELETED:
                yield cell[0]

    def clear(self) -> None:
        self.__length = 0
        self.__deleted = 0
        self.__cells = [None] * self.__capacity

    def get(
            self,
            key: Hashable,
            default: object | None = None
    ) -> object | None:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def pop(
            self,
            key: Hashable,
            default: object | None = None
    ) -> object | None:
        try:
            value = self.__getitem__(key)
        except KeyError:
            return default
        else:
            self.__delitem__(key)
            return value

    def update(self, *args: tuple[Hashable, object] | Dictionary) -> None:
        for data in args:
            if isinstance(data, Dictionary):
                data_cells = [(key, None, data[key]) for key in data]
                if len(data) > self.__capacity * 2:
                    self.__resize(
                        *data_cells,
                        capacity_multiplier_power=0
                    )
                    continue
                for key, _, value, in data_cells:
                    self.__setitem__(key, value)
                continue

            self.__setitem__(*data)




if __name__ == "__main__":
    dictionary = Dictionary(*[(str(i), i * i) for i in range(20)])
    dictionary.update(Dictionary(("k", "val")), ("2", 140))
    print(dictionary["k"])
    for key in dictionary:
        print(key, dictionary[key])
