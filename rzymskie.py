
ROMAN_DICT = {
    "I": 1,
    "V": 5,
    "X": 10,
    "L": 50,
    "C": 100,
    "D": 500,
    "M": 1000
}

def roman_to_arabic(roman_value : str):
    """
    >>> roman_to_arabic("I")
    1
    >>> roman_to_arabic("IX")
    9
    >>> roman_to_arabic("MDL")
    1550
    >>> roman_to_arabic("XIV")
    14
    """
    roman_value.capitalize()
    arabic_value = []

    for letter in roman_value:
        if letter in ROMAN_DICT:
            arabic_value.append(ROMAN_DICT[letter])

    last_value  = ROMAN_DICT["M"] * 2
    cumulative_value = 0

    for value in arabic_value:
        if last_value < value:
            cumulative_value -= 2 * last_value
        cumulative_value += value
        last_value = value

    return cumulative_value


def arabic_to_roman(arabic_value : int):
    """
    >>> arabic_to_roman(1)
    'I'
    >>> arabic_to_roman(10)
    'X'
    >>> arabic_to_roman(9)
    'IX'
    """
    roman_value = ''
    for key, value in ROMAN_DICT:
        pass
    return roman_value


def main():
    import doctest
    doctest.testmod()


if __name__ == "__main__":
    main()