import random
from unittest import mock

import pytest

from app.main import Dictionary
from app.point import Point


@pytest.mark.timeout(5)
def test_deletion():
    items = [(f"Element {i}", i) for i in range(1000)]
    dictionary = Dictionary()
    for key, value in items:
        dictionary[key] = value
    for key, value in items:
        assert dictionary[key] == value
    assert len(dictionary) == len(items)
    for i in range(0, 1000, 2):
        del dictionary[f"Element {i}"]
    assert len(dictionary) == 500
    for i in range(1, 1000, 4):
        del dictionary[f"Element {i}"]
    assert len(dictionary) == 250
#     for key, value in items:
#         del dictionary[key]
#     print(len(dictionary))


@pytest.mark.parametrize(
    "items,pairs_after_adding",
    [
        pytest.param([], [], id="empty dictionary should have len equal to 0"),
        pytest.param(
            [(1, "one"), (2, "two"), (3, "tree"), (4, "four")],
            [(1, "one"), (2, "two"), (3, "tree"), (4, "four")],
            id="integers can be used as keys",
        ),
        pytest.param(
            [(1.1, "one"), (2.2, "two"), (3.3, "tree"), (4.4, "four")],
            [(1.1, "one"), (2.2, "two"), (3.3, "tree"), (4.4, "four")],
            id="floats can be used as keys",
        ),
        pytest.param(
            [("one", 1), ("two", 2), ("tree", 3), ("four", 4)],
            [("one", 1), ("two", 2), ("tree", 3), ("four", 4)],
            id="strings can be used as keys",
        ),
        pytest.param(
            [
                (Point(0, 0), "origin"),
                (Point(10, 10), "A"),
                (Point(-10, 10), "B"),
                (Point(0, 5), "C"),
            ],
            [
                (Point(0, 0), "origin"),
                (Point(10, 10), "A"),
                (Point(-10, 10), "B"),
                (Point(0, 5), "C"),
            ],
            id="Custom hashable classes can be used as keys",
        ),
        pytest.param(
            [("one", 1), (2, [1, 2, 3]), (13.3, 66), (Point(0, 0), "origin")],
            [("one", 1), (2, [1, 2, 3]), (13.3, 66), (Point(0, 0), "origin")],
            id="keys can have different hashable types",
        ),
        pytest.param(
            [
                (8, "8"),
                (16, "16"),
                (32, "32"),
                (64, "64"),
                (128, "128"),
                ("one", 2),
                ("two", 2),
                (Point(1, 1), "a"),
                ("one", 1),
                ("one", 11),
                ("one", 111),
                ("one", 1111),
                (145, 146),
                (145, 145),
                (145, -1),
                ("two", 22),
                ("two", 222),
                ("two", 2222),
                ("two", 22222),
                (Point(1, 1), "A"),
            ],
            [
                (8, "8"),
                (16, "16"),
                (32, "32"),
                (64, "64"),
                (128, "128"),
                ("one", 1111),
                ("two", 22222),
                (145, -1),
                (Point(1, 1), "A"),
            ],
            id="the value should be reassigned when the key already exists",
        ),
    ],
)
def test_dictionary_add(items: list, pairs_after_adding: list):

    dictionary = Dictionary()
    for key, value in items:
        dictionary[key] = value

    for key, value in pairs_after_adding:
        assert dictionary[key] == value
    assert len(dictionary) == len(pairs_after_adding)


@pytest.mark.parametrize(
    "items,pairs_after_adding",
    [
        pytest.param([], [], id="empty dictionary should have len equal to 0"),
        pytest.param(
            [(1, "one"), (2, "two"), (3, "tree"), (4, "four")],
            [(1, "one"), (2, "two"), (3, "tree"), (4, "four")],
            id="integers can be used as keys",
        ),
        pytest.param(
            [
                (Point(0, 0), "origin"),
                (Point(10, 10), "A"),
                (Point(-10, 10), "B"),
                (Point(0, 5), "C"),
            ],
            [
                (Point(0, 0), "origin"),
                (Point(10, 10), "A"),
                (Point(-10, 10), "B"),
                (Point(0, 5), "C"),
            ],
            id="Custom hashable classes can be used as keys",
        ),
        pytest.param(
            [
                (8, "8"),
                (16, "16"),
                (32, "32"),
                ("one", 1),
                ("one", 11),
            ],
            [
                (8, "8"),
                (16, "16"),
                (32, "32"),
                ("one", 11),
            ],
            id="the value should be reassigned when the key already exists",
        ),
    ],
)
@mock.patch("app.main.hash")
def test_dictionary_add_with_mocked_hash(
    mock_hash: mock, items: list, pairs_after_adding: list
):
    mock_hash.return_value = 3

    dictionary = Dictionary()
    for key, value in items:
        dictionary[key] = value

    for key, value in pairs_after_adding:
        assert dictionary[key] == value
    assert len(dictionary) == len(pairs_after_adding)


@pytest.mark.timeout(5)
def test_resize_bucket():
    items = [(f"Element {i}", i) for i in range(1000)]
    dictionary = Dictionary()
    for key, value in items:
        dictionary[key] = value

    for key, value in items:
        assert dictionary[key] == value
    assert len(dictionary) == len(items)


def test_missing_key():
    dictionary = Dictionary()
    with pytest.raises(KeyError):
        dictionary["missing_key"]


def test_is_custom_dict():
    dictionary = Dictionary()
    is_dict = False
    for attr in dictionary.__dict__:
        if type(dictionary.__getattribute__(attr)) == dict:
            is_dict = True
    assert (
        not is_dict
    ), f"You should implement custom dictionary not using built-in dict!!!"


def test_ordering_after_repeating_deletion_insertion():
    keys = [f"Key {i}" for i in range(100)]
    values = list(range(100))
    random.shuffle(keys)

    dictionary = Dictionary()
    dictionary.update(zip(keys, values))

    assert len(dictionary) == len(keys) == 100
    assert sorted(dictionary) == sorted(keys)

    for key_from_dict, key_from_list in zip(dictionary.keys(), keys):
        assert key_from_dict == key_from_list

    for _ in range(20):
        key = random.choice(keys)
        keys.remove(key)
        del dictionary[key]

    assert len(dictionary) == len(keys) == 80

    for i in range(100, 110):
        key = f"Key {i}"
        keys.append(key)
        dictionary[key] = i

    assert len(dictionary) == len(keys) == 90

    for _ in range(20):
        key = random.choice(keys)
        keys.remove(key)
        del dictionary[key]

    assert len(dictionary) == len(keys) == 70

    for key_from_dict, key_from_list in zip(dictionary.keys(), keys):
        assert key_from_dict == key_from_list
