from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional


@dataclass
class _Node:
    key: Any
    key_hash: int
    value: Any


_TOMBSTONE = object()


class Dictionary:
    """
    Dicionário customizado com hash table (lista de nós) e
    tratamento de colisões por linear probing (open addressing).
    """

    def __init__(self, capacity: int = 8, load_factor: float = 0.75) -> None:
        if capacity < 1:
            capacity = 8

        self._capacity: int = max(8, capacity)
        self._load_factor: float = load_factor
        self._size: int = 0

        # Cada célula pode ser:
        # - None (vazio)
        # - _Node (ocupado)
        # - _TOMBSTONE (removido)
        self._table: List[Optional[object]] = [None] * self._capacity

    def __len__(self) -> int:
        return self._size

    def _should_resize(self) -> bool:
        next_load = (self._size + 1) / self._capacity
        return next_load >= self._load_factor

    def _index(self, key_hash: int) -> int:
        return key_hash % self._capacity

    def _find_slot(self, key: Any, key_hash: int) -> int:
        """
        Retorna o índice onde:
        - a chave está (se existir), ou
        - a chave deve ser inserida (primeiro None ou tombstone).
        """
        start: int = self._index(key_hash)
        first_tombstone: Optional[int] = None

        i: int = start
        while True:
            cell = self._table[i]

            if cell is None:
                if first_tombstone is not None:
                    return first_tombstone
                return i

            if cell is _TOMBSTONE:
                if first_tombstone is None:
                    first_tombstone = i
            else:
                node: _Node = cell  # type: ignore[assignment]
                same_hash = node.key_hash == key_hash
                same_key = node.key == key
                if same_hash and same_key:
                    return i

            i = (i + 1) % self._capacity

            if i == start:
                if first_tombstone is not None:
                    return first_tombstone
                raise RuntimeError(
                    "Hashtable cheia: resize não ocorreu como esperado."
                )

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Adiciona ou atualiza um par chave-valor.
        """
        if self._should_resize():
            self._resize()

        key_hash: int = hash(key)
        slot: int = self._find_slot(key, key_hash)

        cell = self._table[slot]
        if cell is None or cell is _TOMBSTONE:
            self._table[slot] = _Node(key=key, key_hash=key_hash, value=value)
            self._size += 1
            return

        node: _Node = cell  # type: ignore[assignment]
        node.value = value

    def __getitem__(self, key: Any) -> Any:
        """
        Retorna o valor associado à chave ou levanta KeyError.
        """
        key_hash: int = hash(key)
        slot: int = self._find_slot(key, key_hash)

        cell = self._table[slot]
        if isinstance(cell, _Node):
            return cell.value

        raise KeyError(key)

    def _resize(self) -> None:
        """
        Dobra a capacidade e reinsere todos os elementos (rehash).
        """
        old_table: List[Optional[object]] = self._table

        self._capacity *= 2
        self._table = [None] * self._capacity
        self._size = 0

        for cell in old_table:
            if isinstance(cell, _Node):
                self[cell.key] = cell.value
