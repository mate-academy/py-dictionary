"""Módulo de implementación de un diccionario personalizado basado en hash."""

from typing import Generic, List, Optional, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class Node(Generic[K, V]):
    """Representa un nodo individual dentro de la tabla hash.

    Almacena la clave original, el valor asociado y el código hash.
    """

    def __init__(self, key: K, value: V, hash_val: int) -> None:
        self.key: K = key
        self.value: V = value
        self.hash_val: int = hash_val


class Dictionary(Generic[K, V]):
    """Implementación personalizada de un diccionario basado en tabla hash.

    Utiliza direccionamiento abierto con sondeo lineal, capacidad inicial
    de 8, factor de carga de 2 / 3 y redimensionamiento dinámico.
    """

    def __init__(
        self, initial_capacity: int = 8, load_factor: float = 2 / 3
    ) -> None:
        self.capacity: int = initial_capacity
        self.load_factor: float = load_factor
        self.size: int = 0
        self.table: List[Optional[Node[K, V]]] = [None] * self.capacity

    def __len__(self) -> int:
        """Retorna el número de elementos almacenados."""
        return self.size

    def _resize(self) -> None:
        """Duplica la capacidad de la tabla y realiza rehash."""
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0

        for node in old_table:
            if node is not None:
                self.__setitem__(node.key, node.value)

    def __setitem__(self, key: K, value: V) -> None:
        """Añade un par clave-valor o actualiza si ya existe."""
        if (self.size + 1) / self.capacity > self.load_factor:
            self._resize()

        h = hash(key)
        index = h % self.capacity
        original_index = index

        while self.table[index] is not None:
            if self.table[index].key == key:
                self.table[index].value = value
                return
            index = (index + 1) % self.capacity
            if index == original_index:
                break

        self.table[index] = Node(key, value, h)
        self.size += 1

    def __getitem__(self, key: K) -> V:
        """Recupera el valor asociado a la clave especificada."""
        h = hash(key)
        index = h % self.capacity
        original_index = index

        while self.table[index] is not None:
            if self.table[index].key == key:
                return self.table[index].value
            index = (index + 1) % self.capacity
            if index == original_index:
                break

        raise KeyError(f"La clave '{key}' no existe en el diccionario.")
