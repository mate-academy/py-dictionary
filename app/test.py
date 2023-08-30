from app.main import Dictionary


def test_dict():
    dict_ = Dictionary()
    dict_.__setitem__(1, "Hello")
    dict_.__setitem__(9, "Hello2")
    dict_.__setitem__(1, "123")
    dict_.__setitem__(2, "g")
    dict_.__setitem__(3, "123")
    dict_.__setitem__(4, "qwe")
    dict_.__setitem__(5, "123")

    assert dict_.__getitem__(1) == "123"
    assert dict_.__getitem__(9) == "Hello2"
    assert dict_.__getitem__(4) == "qwe"
    assert dict_.__getitem__(5) == "123"
    assert dict_.__getitem__(2) == "g"
