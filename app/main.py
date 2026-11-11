from typing import Any


class Node:
    """Representa um nó individual da Hash Table
    guardando chave, hash e valor."""

    def __init__(self, key: Any, hash_value: int, value: Any) -> None:
        self.key = key
        self.hash_value = hash_value
        self.value = value


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.table: list[Node | None] = [None] * capacity
        self.size = 0

    def _index_calculator(self, hash_key: int) -> int:
        return hash_key % self.capacity

    def _load_factor(self) -> float:
        return self.size / self.capacity

    def _should_resize(self) -> bool:
        # Fator de carga > 0.7
        return (self.size + 1) / self.capacity > 0.7

    def __setitem__(self, key: Any, value: Any) -> None:
        hash_key = hash(key)
        index = self._index_calculator(hash_key)

        # 1. Primeiro verifica se a chave já
        # existe na tabela para atualizar o valor
        curr_index = index
        while self.table[curr_index] is not None:
            if self.table[curr_index].key == key:
                self.table[curr_index].value = value
                return
            curr_index = (curr_index + 1) % self.capacity

        # 2. Se for uma nova inserção,
        # verifica se é necessário redimensionar a tabela
        if self._should_resize():
            self._resize()
            index = self._index_calculator(hash_key)
            curr_index = index
            while self.table[curr_index] is not None:
                curr_index = (curr_index + 1) % self.capacity

        # 3. Insere o novo nó no slot livre encontrado
        self.table[curr_index] = Node(key, hash_key, value)
        self.size += 1

    def __getitem__(self, key: Any) -> Any:
        hash_key = hash(key)
        index = self._index_calculator(hash_key)

        curr_index = index
        attempts = 0

        # Sondagem linear para localizar a chave
        while self.table[curr_index] is not None and attempts < self.capacity:
            if self.table[curr_index].key == key:
                return self.table[curr_index].value
            curr_index = (curr_index + 1) % self.capacity
            attempts += 1

        # Se encontrou None ou percorreu a tabela toda, a chave não existe
        raise KeyError(key)

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0

        for item in old_table:
            if item is not None:
                self._place_item(item)

    def _place_item(self, item: Node) -> None:
        index = self._index_calculator(item.hash_value)
        while self.table[index] is not None:
            index = (index + 1) % self.capacity
        self.table[index] = item
        self.size += 1

    def __len__(self) -> int:
        return self.size


# --- CLASSES E FUNÇÕES DE TESTE ---

class SameHash:
    def __init__(self, name: str) -> None:
        self.name = name

    def __hash__(self) -> int:
        return 1

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, SameHash) and self.name == other.name


def test_insert_and_get() -> None:
    dictionary = Dictionary()
    dictionary["a"] = 1
    assert dictionary["a"] == 1
    assert len(dictionary) == 1


def test_update_does_not_increase_size() -> None:
    dictionary = Dictionary()
    dictionary["a"] = 1
    dictionary["a"] = 2
    assert dictionary["a"] == 2
    assert len(dictionary) == 1


def test_collision() -> None:
    first = SameHash("first")
    second = SameHash("second")
    dictionary = Dictionary()
    dictionary[first] = 10
    dictionary[second] = 20
    assert dictionary[first] == 10
    assert dictionary[second] == 20
    assert len(dictionary) == 2
