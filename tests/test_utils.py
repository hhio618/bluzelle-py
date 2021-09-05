from logging import DEBUG, StreamHandler

from bluzelle.utils import bytes_to_str, get_logger, is_string


def test_get_logger():
    logger1 = get_logger("logger1", DEBUG)
    assert logger1.level == DEBUG
    assert logger1.hasHandlers() is True
    assert isinstance(logger1.handlers[0], StreamHandler)


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
