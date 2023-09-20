from typing import Any


class Dictionary:
    def __init__(self, elements: list[tuple[Any, Any]] = None) -> None:
        self.entries = [None for _ in range(8)]
        self.length = 0
        if elements is not None:
            for key, value in elements:
                self[key] = value

    @staticmethod
    def _get_next_index(index: int, iterable: list[Any]) -> int:
        return (index + 1) % len(iterable)

    @staticmethod
    def _get_index(key: Any, iterable: list[Any]) -> int:
        return hash(key) % len(iterable)

    @staticmethod
    def _object_equal(
            input_key: Any,
            input_hash: int,
            entries_key: Any,
            entries_hash: int
    ) -> bool:
        return input_key == entries_key and entries_hash == input_hash

    def _resize_entries(self) -> None:
        new_entries = [None for _ in range(len(self.entries) * 2)]

        for entry in self.entries:
            if entry is not None:
                index = self._get_index(entry[1], new_entries)
                while new_entries[index] is not None:
                    index = self._get_next_index(index, new_entries)
                new_entries[index] = entry

        self.entries = new_entries

    def _need_resize_entries(self) -> bool:
        return self.length / len(self.entries) > 0.6

    def __setitem__(self, input_key: Any, input_value: Any) -> None:
        if self._need_resize_entries():
            self._resize_entries()

        input_hash = hash(input_key)
        index = self._get_index(input_key, self.entries)

        while self.entries[index] is not None:

            entries_hash, entries_key, entries_value = \
                self.entries[index]

            if self._object_equal(
                    input_key,
                    input_hash,
                    entries_key,
                    entries_hash
            ):
                self.entries[index][2] = input_value
                return
            else:
                index = self._get_next_index(index, self.entries)

        self.entries[index] = [input_hash, input_key, input_value]
        self.length += 1

    def __getitem__(self, input_key: Any) -> Any:
        input_hash = hash(input_key)
        index = self._get_index(input_key, self.entries)

        while self.entries[index] is not None:
            entries_hash, entries_key, entries_value = \
                self.entries[index]

            if self._object_equal(
                    input_key,
                    input_hash,
                    entries_key,
                    entries_hash
            ):
                return entries_value
            index = self._get_next_index(index, self.entries)

        raise KeyError(input_key)

    def __len__(self) -> int:
        return self.length
