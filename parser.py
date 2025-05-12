import ply.yacc as yacc
from lexer import tokens  # Make sure lexer.py defines these tokens

# AST Node class
class Node:
    def __init__(self, type, children=None, value=None):
        self.type = type
        self.children = children or []
        self.value = value

    def __repr__(self):
        return f"{self.type}({self.value})" if self.value else f"{self.type}({self.children})"

# Grammar rules
# It’s not hardcoded behavior, it’s defined behavior
def p_program(p):
    "program : INT MAIN LPAREN RPAREN LBRACE stmt_list RBRACE"
    p[0] = Node("main", p[6])

def p_stmt_list(p):
    "stmt_list : stmt_list stmt"
    p[0] = p[1] + [p[2]]

def p_stmt_list_single(p):
    "stmt_list : stmt"
    p[0] = [p[1]]

def p_stmt_decl(p):
    "stmt : INT ID EQUALS expr SEMICOLON"
    p[0] = Node("decl", [Node("id", value=p[2]), p[4]])

def p_stmt_return(p):
    "stmt : RETURN expr SEMICOLON"
    p[0] = Node("return", [p[2]])

def p_expr_plus(p):
    "expr : expr PLUS expr"
    p[0] = Node("add", [p[1], p[3]])

def p_expr_minus(p):
    "expr : expr MINUS expr"
    p[0] = Node("sub", [p[1], p[3]])

def p_expr_number(p):
    "expr : NUMBER"
    p[0] = Node("num", value=p[1])

def p_expr_id(p):
    "expr : ID"
    p[0] = Node("id", value=p[1])

def p_error(p):
    print("Syntax error")

# Build the parser
parser = yacc.yacc()
