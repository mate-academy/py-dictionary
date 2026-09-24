from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from app.main import Node


class DictionaryIterator:
    def __init__(self, table: list["Node | None"]) -> None:
        self._table = table
        self._index = 0

    def __iter__(self) -> DictionaryIterator:
        return self

    def __next__(self) -> Any:
        while self._index < len(self._table):
            node = self._table[self._index]
            self._index += 1
            if node is not None:
                return node.key

        raise StopIteration
