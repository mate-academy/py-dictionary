import pytest

from app.main import Dictionary


def test_delitem() -> None:
    d = Dictionary()
    d["a"] = 1
    d["b"] = 2
    del d["a"]
    assert "a" not in d
    assert len(d) == 1
    with pytest.raises(KeyError):
        del d["a"]


def test_clear() -> None:
    d = Dictionary()
    d["a"] = 1
    d["b"] = 2
    d.clear()
    assert len(d) == 0
    assert "a" not in d
    assert "b" not in d


def test_get() -> None:
    d = Dictionary()
    d["a"] = 1
    assert d.get("a") == 1
    assert d.get("b") is None
    assert d.get("b", "default") == "default"


def test_contains() -> None:
    d = Dictionary()
    d["a"] = 1
    assert "a" in d
    assert "b" not in d


def test_pop() -> None:
    d = Dictionary()
    d["a"] = 1
    d["b"] = 2
    assert d.pop("a") == 1
    assert "a" not in d
    assert len(d) == 1
    with pytest.raises(KeyError):
        d.pop("a")
    assert d.pop("c", "default") == "default"
    with pytest.raises(TypeError):
        d.pop("a", "b", "c")


def test_update() -> None:
    d = Dictionary()
    d.update({"a": 1, "b": 2})
    assert d["a"] == 1
    assert d["b"] == 2
    d.update([("c", 3), ("d", 4)])
    assert d["c"] == 3
    assert d["d"] == 4


def test_iter() -> None:
    d = Dictionary()
    d["a"] = 1
    d["b"] = 2
    keys = set()
    for key in d:
        keys.add(key)
    assert keys == {"a", "b"}
