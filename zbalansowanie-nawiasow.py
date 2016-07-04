
BRACES_LIST = ['{', '}', '[', ']', '(', ')','<','>']


def zbalansowanie_nawiasow(reference : str):
    """
    >> > zbalansowanie_nawiasow("() [] () ([]()[])")
    True
    >> > zbalansowanie_nawiasow("( (] ([)]")
    False
    """
    parse_string = ''
    stack = []
    is_balanced = True

    for symbol in reference:
        if symbol in BRACES_LIST:
            parse_string.append(symbol)

    for brace in parse_string:
        if (BRACES_LIST.index(brace)%2):
            stack.append(BRACES_LIST.index(brace))
        else:
            #TODO: handle stack.pop() error
            if (stack.pop() != (BRACES_LIST.index(brace) - 1)):
                return False


    return is_balanced

def main():
    import doctest
    doctest.testmod()


if __name__ == "__main__":
    main()