
from decimal import Decimal

import pytest
from smd_decoder.eia96 import decode, decode_scale

def test_decode_scale():
    for v in range(0,7):
        ch = chr(ord('A') + v)
        assert decode_scale(ch) == v
    assert decode_scale("X") == -1
    assert decode_scale("Y") == -2
    assert decode_scale("Z") == -3

@pytest.mark.parametrize("code, ohms", [
    ("01C", "10000"),
    ("01B", "1000"),
    ("01Y", "1"),
    ("36H", "2320"),
    ("68X", "49.9"),
    ("85Z", "0.75"),
])
def test_decode(code, ohms):
    assert decode(code) == Decimal(ohms)

