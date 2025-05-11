from lexer import lexer

code = '''
int main() {
    int x = 10;
    if (x > 5) {
        return x;
    }
}
'''

lexer.input(code)

print("Tokens:")
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
