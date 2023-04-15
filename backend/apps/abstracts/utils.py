import random


# generate activation code
def generate_code(code_len: int) -> str:
    digits: str = '0123456789'
    alfabet: str = 'ABCDEFGHJKLMNOPQRSTVWXYZ'
    symbols: str = digits + alfabet
    code: list = [symbols[random.randrange(0, len(symbols))] for _ in range(code_len)]  # noqa

    return ''.join(code)
