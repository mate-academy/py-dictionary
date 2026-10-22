"""Módulo de implementación de un diccionario personalizado."""

from typing import Any, Generic, List, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class Node(Generic[K, V]):
    """Representa un nodo individual dentro de la tabla hash.

    Almacena la clave original, el valor y el hash.
    """

    def __init__(self, key: K, value: V, hash_val: int) -> None:
        self.key: K = key
        self.value: V = value
        self.hash_val: int = hash_val


class Dictionary(Generic[K, V]):
    """Implementación personalizada de un diccionario."""

    def __init__(
        self, initial_capacity: int = 8, load_factor: float = 2 / 3
    ) -> None:
        self.capacity: int = initial_capacity
        self.load_factor: float = load_factor
        self.length: int = 0
        self._DELETED: Any = object()
        self.hash_table: List[Any] = [None] * self.capacity

    def __len__(self) -> int:
        """Retorna el número de elementos."""
        return self.length

    def _resize(self) -> None:
        """Duplica capacidad y realiza rehash eficiente."""
        old_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.length = 0

        for item in old_table:
            if item is not None and item is not self._DELETED:
                index = item.hash_val % self.capacity
                original_index = index
                while self.hash_table[index] is not None:
                    index = (index + 1) % self.capacity
                    if index == original_index:
                        break
                self.hash_table[index] = item
                self.length += 1

    def __setitem__(self, key: K, value: V) -> None:
        """Añade un par clave-valor o actualiza si existe."""
        if (self.length + 1) / self.capacity > self.load_factor:
            self._resize()

        h = hash(key)
        index = h % self.capacity
        original_index = index
        first_deleted_index = None

        while self.hash_table[index] is not None:
            if self.hash_table[index] is self._DELETED:
                if first_deleted_index is None:
                    first_deleted_index = index
            elif self.hash_table[index].key == key:
                self.hash_table[index].value = value
                return
            index = (index + 1) % self.capacity
            if index == original_index:
                break

        target_index = (
            first_deleted_index
            if first_deleted_index is not None
            else index
        )
        if (
            self.hash_table[target_index] is None
            or self.hash_table[target_index] is self._DELETED
        ):
            self.hash_table[target_index] = Node(key, value, h)
            self.length += 1

    def __getitem__(self, key: K) -> V:
        """Recupera el valor asociado a la clave."""
        h = hash(key)
        index = h % self.capacity
        original_index = index

        while self.hash_table[index] is not None:
            if self.hash_table[index] is not self._DELETED:
                if self.hash_table[index].key == key:
                    return self.hash_table[index].value
            index = (index + 1) % self.capacity
            if index == original_index:
                break

        raise KeyError(f"La clave '{key}' no existe en el diccionario.")

    def __delitem__(self, key: K) -> None:
        """Elimina una clave y su valor."""
        h = hash(key)
        index = h % self.capacity
        original_index = index

        while self.hash_table[index] is not None:
            if self.hash_table[index] is not self._DELETED:
                if self.hash_table[index].key == key:
                    self.hash_table[index] = self._DELETED
                    self.length -= 1
                    return
            index = (index + 1) % self.capacity
            if index == original_index:
                break

        raise KeyError(f"La clave '{key}' no existe en el diccionario.")

    def get(self, key: K, default: Any = None) -> Any:
        """Retorna el valor si la clave existe, de lo contrario default."""
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def pop(self, key: K, *args: Any) -> V:
        """Elimina la clave y retorna su valor, o maneja default."""
        try:
            value = self.__getitem__(key)
            self.__delitem__(key)
            return value
        except KeyError:
            if args:
                return args[0]
            raise
