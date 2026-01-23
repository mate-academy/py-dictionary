from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.storage = [None] * self.capacity
        self.current_length = 0

    def __len__(self) -> int:
        return self.current_length

    def size_storage(self) -> None:
        """This method keeps track of the storage size."""
        current_limit = int(self.capacity * (2 / 3))
        if self.current_length >= current_limit:
            self.capacity *= 2
            self.rehash()

    def rehash(self) -> None:
        """
        This method resizes the storage and sends the key
        and value to the __setitem__ method for re-allocation.
        """
        old_storage = self.storage
        self.storage = [None] * self.capacity
        self.current_length = 0

        for element in old_storage:
            if element is not None:
                key, value = element[0], element[1]
                self.__setitem__(key, value)

    def get_index_hash(self, key: Hashable) -> tuple[int, int]:
        """This method calculates the index for storage and the hash."""
        hash_ = hash(key)
        index_ = hash_ % self.capacity
        return hash_, index_

    def collision(self, key: Hashable, index_: int) -> int:
        """This method deals with collisions."""
        for i in range(self.capacity):
            new_index = (index_ + i) % self.capacity
            if (self.storage[new_index] is None
                    or self.storage[new_index][0] == key):
                return new_index

    def __setitem__(self, key: Hashable, value: Any) -> None:
        """
        This method is responsible for placing
        the key-value-hash tuple into storage.
        """
        self.size_storage()
        hash_, index_ = self.get_index_hash(key)

        if self.storage[index_] is None:
            self.storage[index_] = (key, value, hash_)
            self.current_length += 1
        else:
            if self.storage[index_][0] == key:
                self.storage[index_] = (key, value, hash_)
            else:
                new_index = self.collision(key, index_)
                if self.storage[new_index] is None:
                    self.storage[new_index] = (key, value, hash_)
                    self.current_length += 1
                else:
                    self.storage[new_index] = (key, value, hash_)

    def get_key_index(self, key: Hashable) -> int:
        """This method finds the key for
        the pop, __getitem__ and __delitem__ methods."""
        hash_, index_ = self.get_index_hash(key)

        if self.storage[index_] is None:
            raise KeyError("No such key exists.")

        if (self.storage[index_][0] == key
                and self.storage[index_][2] == hash_):
            return index_

        for i in range(1, self.capacity):
            new_index = (index_ + i) % self.capacity
            if self.storage[new_index] is None:
                raise KeyError("No such key exists.")
            if (self.storage[new_index][0] == key
                    and self.storage[new_index][2] == hash_):
                return new_index

    def __getitem__(self, key: Hashable) -> Any:
        """This method is responsible for getting the value by key."""
        index_ = self.get_key_index(key)
        return self.storage[index_][1]

    def clear(self) -> None:
        """This method returns the dictionary to its original form."""
        self.capacity = 8
        self.storage = [None] * self.capacity
        self.current_length = 0

    def __delitem__(self, key: Hashable) -> None:
        """This method removes an element by the specified key."""
        index_ = self.get_key_index(key)
        self.storage[index_] = None
        self.current_length -= 1

    def get(self, key: Hashable, user_value: Any = None) -> None | Any:
        """This method returns the value by key or None | user value."""
        try:
            return self.__getitem__(key)
        except KeyError:
            return user_value

    def __iter__(self) -> Any:
        """This method returns keys when iterating over a dictionary."""
        for element in self.storage:
            if element is not None:
                yield element[0]

    def pop(self, key: Hashable, user_value: Any = None) -> Any:
        """This method returns the value by key and removes the element."""
        try:
            index_ = self.get_key_index(key)
            value = self.storage[index_][1]
            self.__delitem__(key)
            return value
        except KeyError:
            if user_value is not None:
                return user_value
            else:
                raise KeyError("No such key exists.")
