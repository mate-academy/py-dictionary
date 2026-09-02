from collections.abc import Hashable, Iterable, Iterator, Mapping
from dataclasses import dataclass
from typing import Any, overload


@dataclass
class Node:
    """Представляє вузол для збереження пари ключ-значення у словнику.

    Attributes:
        key: Об'єкт ключа, що підтримує хешування (Hashable).
        value: Значення, асоційоване з ключем.
        hash_key: Попередньо обчислений хеш ключа.
    """
    key: Hashable
    value: Any | None
    hash_key: int


class Dictionary:
    """Кастомна реалізація хеш-мапи"""

    DEFAULT_CAPACITY = 8
    LOAD_FACTOR = 0.75

    def __init__(self, capacity: int = DEFAULT_CAPACITY) -> None:
        """Ініціалізує екземпляр Dictionary з заданою місткістю."""
        self.capacity = capacity
        self.buckets: list[list[Node]] = [[] for _ in range(capacity)]
        self.size = 0
        self.threshold = self.capacity * self.LOAD_FACTOR

    def __getitem__(self, key: Hashable) -> Any:
        """Повертає значення, що відповідає заданому ключу.

        Raises:
            KeyError: Якщо ключ відсутній у словнику.
        """
        _, _, node = self._find(key)
        if node is not None:
            return node.value
        raise KeyError(f"Key {key!r} is not found in dictionary.")

    def __setitem__(self, key: Hashable, value: Any) -> None:
        """Додає нову пару ключ-значення або оновлює
                                значення для існуючого ключа."""
        bucket, _, node = self._find(key)
        if node is not None:
            node.value = value
            return

        key_hash = hash(key)
        bucket.append(Node(key=key, value=value, hash_key=key_hash))
        self.size += 1
        if self.size > self.threshold:
            self._resize()

    def __len__(self) -> int:
        """Повертає загальну кількість елементів у словнику."""
        return self.size

    def clear(self) -> None:
        """Видаляє всі елементи зі словника
                    та скидає місткість до дефолтної."""
        self.capacity = self.DEFAULT_CAPACITY
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0
        self.threshold = self.capacity * self.LOAD_FACTOR

    def __delitem__(self, key: Hashable) -> None:
        """Видаляє елемент за ключем.

        Raises:
            KeyError: Якщо ключ відсутній у словнику.
        """
        bucket, i, node = self._find(key)
        if node is not None and i is not None:
            bucket.pop(i)
            self.size -= 1
            return
        raise KeyError(f"Key {key!r} is not found in dictionary.")

    def get(self, key: Hashable, default: Any = None) -> Any:
        """Повертає значення за ключем, або значення за замовчуванням
                                            (default), якщо ключ відсутній."""
        _, _, node = self._find(key)
        return node.value if node is not None else default

    def pop(self, key: Hashable, default: Any = ...) -> Any:
        """Видаляє ключ із словника та повертає його значення.

        Raises:
            KeyError: Якщо ключ відсутній і параметр default не передано.
        """
        bucket, i, node = self._find(key)
        if node is not None and i is not None:
            value = node.value
            bucket.pop(i)
            self.size -= 1
            return value
        if default is not ...:
            return default
        raise KeyError(f"Key {key!r} is not found in dictionary.")

    def __iter__(self) -> Iterator[Hashable]:
        """Повертає ітератор, який послідовно
                                    проходить по всіх ключах у бакетах."""
        for bucket in self.buckets:
            for node in bucket:
                yield node.key

    def _find(
            self, key: Hashable
    ) -> tuple[list[Node], int | None, Node | None]:
        """Внутрішній допоміжний метод для пошуку бакета,
                                                індексу та вузла за ключем."""
        index = hash(key) % self.capacity
        bucket = self.buckets[index]
        for i, node in enumerate(bucket):
            if node.key == key:
                return bucket, i, node
        return bucket, None, None

    def _resize(self) -> None:
        """Збільшує місткість таблиці вдвічі
                                та перерозподіляє існуючі вузли."""
        old_buckets = self.buckets
        self.capacity *= 2
        self.threshold = self.capacity * self.LOAD_FACTOR
        self.buckets = [[] for _ in range(self.capacity)]

        for bucket in old_buckets:
            for node in bucket:
                new_index = node.hash_key % self.capacity
                self.buckets[new_index].append(node)

    @overload
    def update(self, m: Mapping[Hashable, Any], /, **kwargs: Any) -> None:
        ...

    @overload
    def update(self, m: Iterable[tuple[Hashable, Any]], /,
               **kwargs: Any) -> None:
        ...

    @overload
    def update(self, **kwargs: Any) -> None:
        ...

    def update(
            self,
            other: Mapping[Hashable, Any] | Iterable[
                tuple[Hashable, Any]] | None = None,
            **kwargs: Any
    ) -> None:
        """Оновлює словник парами ключ-значення з іншого об'єкта або kwargs.

        Перевантаження (@overload) додані для автодоповнення в IDE
        та щоб flake8 / тайп-чекери не видавали помилок через гнучкі типи.

        Args:
            other: Словник (Mapping) або ітерований об'єкт пар (key, value).
            **kwargs: Додаткові пари ключ-значення, передані як аргументи.

        Raises:
            TypeError: Якщо тип `other` не підтримується для ітерації.
        """
        if other is not None:
            if isinstance(other, Mapping) or hasattr(other, "keys"):
                for key in other.keys():
                    self[key] = other[key]
            elif hasattr(other, "items"):
                for key, value in other.items():
                    self[key] = value
            else:
                for key, value in other:
                    self[key] = value

        for key, value in kwargs.items():
            self[key] = value
