from bluzelle.utils import bytes_to_str, is_string


def test_is_string():
    assert is_string("dsfdsfsf") is True
    assert is_string(12312) is False
    assert is_string([]) is False
    assert is_string(b"\x22\x33\x44") is True


def test_bytes_to_str():
    test_str = b"sfsefsfsf"
    test_bytes = b"\x22\x33\x44"
    assert bytes_to_str(test_str) == "sfsefsfsf"
    assert bytes_to_str(test_bytes) == '"3D'
