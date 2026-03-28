from dataclasses import dataclass
from typing import Any, Hashable


class DictSettings:
    load_factor = 2 / 3
    capacity = 8

    @classmethod
    def change_load_factor(cls, new_load_factor: float) -> None:
        """Change the load factor for new class objects."""

        cls.load_factor = new_load_factor
        print(
            f"Load factor was changed for new classes objects to "
            f"{new_load_factor}."
            " Please remember, the default 'load factor' is '2/3'."
        )

    @classmethod
    def change_capacity(cls, new_capacity: int) -> None:
        """Change the capacity for new class objects."""

        cls.capacity = new_capacity
        print(
            f"Load factor was changed for new classes objects to "
            f"{new_capacity}."
            " Please remember, the default 'capacity' is '8'."
        )


@dataclass
class Node:
    key: Hashable
    value: Any
    hash_value: int

    def __repr__(self) -> Any:
        return hash(self.key)
