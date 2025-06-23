import ply.yacc as yacc
#bottom up, LALR(1)
from lexer import tokens 

class Node:
    def __init__(self, type, children=None, value=None):
        self.type = type
        self.children = children or []
        self.value = value
    def __repr__(self):
        return f"{self.type}({self.value})" if self.value else f"{self.type}({self.children})"

precedence = (
    ('left', 'EQ', 'NE'),
    ('left', 'LT', 'GT', 'LE', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIV'),    #lower lines have higher precedence
)

symbol_table = {}
start = 'program'

def p_program(p):               # function name is the rule name
    "program : INT MAIN LPAREN RPAREN LBRACE stmt_list RBRACE"
    p[0] = Node("main", p[6])

def p_stmt_list(p):
    '''stmt_list : stmt        
                 | stmt_list stmt'''  #matches either a single statement or multiple stmt
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_stmt_decl(p):
    "stmt : INT ID ASSIGN expr SEMI"
    var_name = p[2]
    # Add to symbol table
    symbol_table[var_name] = {"type": "int"}
    p[0] = Node("decl", [Node("id", value=p[2]), p[4]])

def p_stmt_return(p):
    "stmt : RETURN expr SEMI"
    p[0] = Node("return", [p[2]])

def p_stmt_if(p):
    "stmt : IF LPAREN expr RPAREN LBRACE stmt_list RBRACE"
    p[0] = Node("if", [p[3], p[6]])

def p_stmt_if_else(p):
    "stmt : IF LPAREN expr RPAREN LBRACE stmt_list RBRACE ELSE LBRACE stmt_list RBRACE"
    p[0] = Node("if_else", [p[3], p[6], p[10]])

def p_expr_plus(p):
    "expr : expr PLUS expr"
    p[0] = Node("add", [p[1], p[3]])

def p_expr_minus(p):
    "expr : expr MINUS expr"
    p[0] = Node("sub", [p[1], p[3]])

def p_expr_eq(p):
    "expr : expr EQ expr"
    p[0] = Node("eq", [p[1], p[3]])

def p_expr_ne(p):
    "expr : expr NE expr"
    p[0] = Node("ne", [p[1], p[3]])

def p_expr_lt(p):
    "expr : expr LT expr"
    p[0] = Node("lt", [p[1], p[3]])

def p_expr_gt(p):
    "expr : expr GT expr"
    p[0] = Node("gt", [p[1], p[3]])

def p_expr_le(p):
    "expr : expr LE expr"
    p[0] = Node("le", [p[1], p[3]])

def p_expr_ge(p):
    "expr : expr GE expr"
    p[0] = Node("ge", [p[1], p[3]])

def p_expr_number(p):
    "expr : NUMBER"
    p[0] = Node("num", value=p[1])

def p_expr_id(p):
    "expr : ID"
    p[0] = Node("id", value=p[1])

def p_error(p):
    print("Syntax error")

parser = yacc.yacc()
