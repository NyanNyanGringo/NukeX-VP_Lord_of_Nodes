

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


def auto_enter(text):
    words = text.split()
    new_text = ''
    char_count = 0

    for word in words:
        word_len = len(word)

        # Check if adding the current word would exceed the 100-character limit
        if char_count + word_len > 50:
            new_text += '\n'
            char_count = 0

        # Append the word to the new text
        new_text += word + ' '
        char_count += word_len + 1

    return new_text.strip()
