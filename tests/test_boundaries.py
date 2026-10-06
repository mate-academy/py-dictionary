import pytest

from app.main import Dictionary


class CollidingKey:
    def __init__(self, number: int) -> None:
        self.number = number

    def __hash__(self) -> int:
        return -7

    def __eq__(self, other: object) -> bool:
        return isinstance(other, CollidingKey) and self.number == other.number


def test_collisions_survive_repeated_resizing() -> None:
    dictionary = Dictionary()
    for number in range(200):
        dictionary[CollidingKey(number)] = number
    for number in range(200):
        assert dictionary[CollidingKey(number)] == number
    dictionary[CollidingKey(100)] = "updated"
    assert dictionary[CollidingKey(100)] == "updated"
    assert len(dictionary) == 200
    with pytest.raises(KeyError):
        dictionary[CollidingKey(201)]


def test_equal_numeric_keys_share_one_entry() -> None:
    dictionary = Dictionary()
    dictionary[1] = "integer"
    dictionary[True] = "boolean"
    assert dictionary[1.0] == "boolean"
    assert len(dictionary) == 1


def test_same_nan_object_remains_retrievable() -> None:
    dictionary = Dictionary()
    key = float("nan")
    dictionary[key] = None
    assert dictionary[key] is None
    dictionary[key] = "updated"
    assert len(dictionary) == 1
    assert dictionary[key] == "updated"


def test_unhashable_keys_raise_type_error() -> None:
    dictionary = Dictionary()
    with pytest.raises(TypeError):
        dictionary[[]] = 1
    with pytest.raises(TypeError):
        dictionary[[]]
