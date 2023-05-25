

def check_symbol_is_english(symbol):
    """
    Check if symbol is English or not
    :param symbol: str
    :return: bool
    """
    try:
        symbol.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True
