import pytest
from smd_decoder.smd_decoder import decode
from decimal import Decimal

@pytest.mark.parametrize("code, ohms", [
    ("103", "10000"),
    ("1002", "10000"),
    ("01c", "10000"),
    ("4r7", "4.7"),
    ("0R22", "0.22"),
    ("R100", "0.1"),
    ("000", "0"),
    ("472", "4700"),
    ("18A", "120"),
])
def test_decode(code, ohms):
    assert decode(code) == Decimal(ohms)
