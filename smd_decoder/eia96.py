import decimal

SCALE_LOOKUP = {
    "H": 1,
    "R": -2,
    "S": -1
}

def decode_value(code:int) -> int:
    return round(10 ** ((191+code)/96))

def decode_scale(scale:str) -> int:
    su = scale[0].upper()
    if (lv := SCALE_LOOKUP.get(su, None)) is not None:
        return lv
    else:
        ch = ord(su)
        return ch - ord("A") if ch < ord("X") else ord("X") - ch - 1
    

def decode(code: str) -> decimal.Decimal:
    return decimal.Decimal(decode_value(int(code[0:2]))).scaleb(decode_scale(code[2]))
