from lexer import lexer

def main():
    # Sample C-like input string
    test_code = '''
    int x = 10;
    int y = x + 20;
    if (y > 25) {
        y = y - 1;
    } else {
        y = y + 1;
    }
    return y;
    '''

    # Feed the input to the lexer
    lexer.input(test_code)

    # Tokenize and print each token
    print("Tokens:")
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(f"Line {tok.lineno}: {tok.type}({tok.value})")

if __name__ == "__main__":
    main()
