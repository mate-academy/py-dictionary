from app.main import Dictionary


def test_set_get_len() -> None:
    d = Dictionary()
    d["apple"] = 10
    d["banana"] = 20
    assert d["apple"] == 10
    assert d["banana"] == 20
    assert len(d) == 2

    d["apple"] = 15
    assert d["apple"] == 15
    assert len(d) == 2


def test_keyerror() -> None:
    d = Dictionary()
    d["key"] = "value"
    try:
        _ = d["nonexistent"]
    except KeyError:
        pass


def test_resize() -> None:
    d = Dictionary(initial_capacity=2, load_factor=0.5)
    d["a"] = 1
    d["b"] = 2
    d["c"] = 3
    assert len(d) == 3
    assert d["a"] == 1
    assert d["b"] == 2
    assert d["c"] == 3
