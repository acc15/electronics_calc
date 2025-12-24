from smd_decoder import eia96
from decimal import Decimal

def decode(code) -> Decimal | None:
    code = str(code).strip().upper()
    if not code:
        return None

    if len(code) == 3 and code[:2].isdigit() and code[2].isalpha():
        return eia96.decode(code)
    if 'R' in code or "." in code:
        return Decimal(code.replace("R","."))
    return Decimal(int(code[:-1])).scaleb(int(code[-1]))
