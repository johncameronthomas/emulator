def assemble(code):
    code = code.replace('\n', '')
    code = code.replace(';', ' ')
    tokens = code.split(' ')
    tokens = tokens[:-1]

    print(tokens)

    symbols = {
        'no_op': 0,
        'halt': 1,
        'move': 2,
        'create': 3,
        'load': 4,
        'store': 5,
        'store_i': 6,
        'jump': 7,
        'jump_i': 8,
        'jump_if_equal': 9,
        'jump_i_if_equal': 10,
        'jump_if_equal_i': 11,
        'jump_i_if_equal_i': 12,
        'link': 13,
        'not': 14,
        'and': 15,
        'and_i': 16,
        'or': 17,
        'or_i': 18,
        'xor': 19,
        'xor_i': 20
    }

    for index, token in enumerate(tokens):
        if token[0] == '@':
            symbols['!' + token[1:]] = index
            del tokens[index]

    program = []

    for token in tokens:
        try:
            program.append(symbols[token])
        except:
            program.append(int(token))

    return tuple(program)