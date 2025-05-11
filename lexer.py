import ply.lex as lex

tokens = (
    'ID', 'NUMBER',  # Identifiers (e.g., variable or function names), Numeric literals (e.g., 42, 100)
    'PLUS', 'MINUS', 'MULT', 'DIV',  # Arithmetic operators (+, -, *, /)
    'ASSIGN',  # Assignment operator (=)
    'SEMI',  # Semicolon (;), used to terminate statements    
    'LPAREN', 'RPAREN',  # Parentheses (for grouping expressions or function calls)   
    'LBRACE', 'RBRACE',  # Braces ({}, used to define code blocks)
    'IF', 'ELSE', 'WHILE', 'RETURN', 'INT'  # Keywords ('if', 'else', 'while', 'return', 'int')
)


#maps the given reserved keyword to the corresponding token
reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'return': 'RETURN',
    'int': 'INT'
}


#In PLY, t_ stands for "token rule".
#The r stands for "raw string" in Python.
#r'\+' is a regular expression (regex) that says "look for a plus sign (+)."
#The backslash (\) is used to escape special characters in regex.
#+ normally means "one or more" in regex, so we escape it to match the literal character +

#Each line is a token rule.
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_MULT    = r'\*'
t_DIV     = r'/'
t_ASSIGN  = r'='
t_SEMI    = r';'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE  = r'\{'
t_RBRACE  = r'\}'

#➡️ When the lexer sees a + in the input code, it will generate a token like:
#Token(type='PLUS', value='+')



#PLY sets t.type automatically based on the function name.
#So if your function is called t_NUMBER, PLY will automatically assign t.type = 'NUMBER'.
#You only need to manually override t.type when there's ambiguity — like in t_ID, where it could be a keyword or an identifier.


# Complex rules
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words (t.value is the actual text)
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)                # Converts the string '123' into the integer 123, so the token stores it as a number.
    return t

# Ignored characters (spaces and tabs)
t_ignore = ' \t'

# Newline tracking
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


lexer = lex.lex()   #It tells PLY to scan the current Python module (where this line appears) and find all the functions and variables needed to build the lexer.
#You can now use this object to tokenize input strings using lexer.input("your_code_here") and retrieve tokens using lexer.token().