from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import MutableMapping, Mapping
from typing import Any, Hashable, Generator, Iterable

_SENTINEL = object()


class IHasKeys(ABC):
    @abstractmethod
    def keys(self) -> Generator:
        pass

    @abstractmethod
    def __getitem__(self, key: Hashable) -> Any:
        pass


class ListNode:
    def __init__(
            self,
            key: Hashable,
            key_hash : int | None = None,
            value: Any = None,
            next_node: ListNode = None,
            before: ListNode = None,
            after: ListNode = None
    ) -> None:
        self.key = key
        self.key_hash = key_hash or hash(key)
        self.value = value
        self.next = next_node  # keep order if collision occurs
        self.before = before   # keep order of insertions
        self.after = after     # keep order or insertions

    def __repr__(self) -> str:
        return f"({self.key}, {self.key_hash}, {self.value}) -> {self.next}"


class Dictionary(MutableMapping, IHasKeys):
    """
    It is an ordered dictionary.
    The main idea of this dictionary is to keep all keys and values
    inside ListNodes that are placed in internal hash table (list).

    In the case of collisions, we form single connected Linked List
    from ListNodes (attribute `next` points to the next ListNode).

    Also, we keep all our existing nodes in order they were added
    to the list due to attributes `before` and `after`.
    They form a doubly linked list which starts from
    self.ordering_head and ends with self.ordering_tail.
    """
    def __init__(self, *args, **kwargs) -> None:
        self.capacity: int = 8
        self.length: int = 0
        self.load_factor: float = 2 / 3
        self.hash_table: list[ListNode | None] = [None] * self.capacity

        self.ordering_head = ListNode(0)
        self.ordering_tail = ListNode(0, before=self.ordering_head)
        self.ordering_head.after = self.ordering_tail

        for key in args:
            self[key] = None

        for key, value in kwargs.items():
            self[key] = value

    def __contains__(self, key: Hashable) -> bool:
        idx = hash(key) % self.capacity
        head = self.hash_table[idx]

        while head:
            if head.key == key:
                return True
            head = head.next

        return False

    def __setitem__(self, key: Hashable, value: Any) -> None:
        node = self.__get_node(key)

        if node:
            node.value = value
            return

        key_hash = hash(key)
        idx = key_hash % self.capacity

        head = self.hash_table[idx]
        new_node = ListNode(key, key_hash, value)
        if head is None:  # there is no node in hashtable at idx
            self.hash_table[idx] = new_node
        else:
            while head.next:  # go to tail if there are nodes
                head = head.next
            head.next = new_node

        self.__add_to_ordering_end(new_node)

        self.length += 1
        if self.length / self.capacity > self.load_factor:
            self.__resize()

    def __getitem__(self, key: Hashable) -> Any:
        node = self.__get_node(key)

        if not node:
            raise KeyError(f"Key {key} not found")

        return node.value

    def __delitem__(self, key: Hashable) -> None:
        node_to_del = self.__get_node(key)

        if not node_to_del:
            raise KeyError(f"Key {key} not found")

        idx = hash(key) % self.capacity
        head = self.hash_table[idx]

        if head == node_to_del:
            self.hash_table[idx] = head.next
        else:
            while head.next:
                if head.next == node_to_del:
                    head.next = head.next.next
                    break
                head = head.next

        self.__delete_from_ordering(node_to_del)
        self.length -= 1

    def __len__(self) -> int:
        return self.length

    def __iter__(self) -> Generator[Hashable, None, None]:
        curr_node = self.ordering_head.after
        while curr_node is not self.ordering_tail:
            yield curr_node.key
            curr_node = curr_node.after

    def __delete_from_ordering(self, node: ListNode) -> None:
        """
        Deleting node from double linked ordering list.
        :param node: ListNode: node to delete
        :return: None
        """
        previous = node.before
        following = node.after

        previous.after = following
        following.before = previous

    def __add_to_ordering_end(self, node: ListNode) -> None:
        tail = self.ordering_tail.before

        tail.after = node
        node.before = tail

        node.after = self.ordering_tail
        self.ordering_tail.before = node

    def __get_node(self, key: Hashable) -> ListNode | None:
        """
        Get node by key
        :param key: Hashable: key of the dictionary
        :return: ListNode or None
        """
        idx = hash(key) % self.capacity
        head = self.hash_table[idx]

        while head:
            if head.key == key:
                return head
            head = head.next

        return None

    def __resize(self) -> None:
        """
        Increase the capacity of internal hash table.
        :return: None
        """
        self.capacity *= 2
        new_hash_table: list = [None] * self.capacity

        for node in self.hash_table:
            while node is not None:
                new_idx = node.key_hash % self.capacity
                tail = new_hash_table[new_idx]

                if tail is None:
                    new_hash_table[new_idx] = node
                else:
                    while tail.next:
                        tail = tail.next
                    tail.next = node

                node.next, node = None, node.next

        self.hash_table = new_hash_table

    def clear(self) -> None:
        """
        Clear this dictionary.
        :return: None
        """
        self.length = 0
        for i in range(self.capacity):
            self.hash_table[i] = None

    def get(self, key: Hashable, default: Any = None) -> Any:
        """
        Get item by key or return default if key is not found.
        :param key: Hashable: key of the dictionary
        :param default: Any: default value to return if key is not found
        :return: Any: found value or default
        """
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Hashable, default: Any = _SENTINEL) -> Any:
        """
        get item by key or return default if key is not found
        and delete key from hash table.
        :param key: Hashable: key of the dictionary
        :param default:  Any: default value to return if key is not found
        :return: Any: found value or default
        """
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            if default is _SENTINEL:
                raise
            return default

    def update(
            self,
            other: Mapping | IHasKeys | Iterable = (),
            /,
            **kwords
    ) -> None:
        """
        update this dictionary from:
            another Mapping,
            object with keys(),
            or sequence of key-value pairs (like tuples or so),
            or from keyword arguments

        :param other: object with keys(), or sequence of key-value pairs
        :param kwords: key-value arguments
        :return: None
        """
        if isinstance(other, Mapping):
            for key in other:
                self[key] = other[key]
        elif hasattr(other, "keys"):
            for key in other.keys():
                self[key] = other[key]
        else:
            for key, value in other:
                self[key] = value
        for key, value in kwords.items():
            self[key] = value

    def keys(self) -> Generator[Hashable, None, None]:
        curr_node = self.ordering_head.after
        while curr_node is not self.ordering_tail:
            yield curr_node.key
            curr_node = curr_node.after

    def values(self) -> Generator[Any, None, None]:
        curr_node = self.ordering_head.after
        while curr_node is not self.ordering_tail:
            yield curr_node.value
            curr_node = curr_node.after

    def items(self) -> Generator[tuple[Hashable, Any], None, None]:
        curr_node = self.ordering_head.after
        while curr_node is not self.ordering_tail:
            yield (curr_node.key, curr_node.value)
            curr_node = curr_node.after
