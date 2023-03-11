'''
Define Verilog tokens and module item types
'''

# token types
MODULE = 'module'
ENDMODULE = 'endmodule'
IDENTIFIER = 'identifier'
PORT = 'port'
SEMICOLON = ';'
LRANGE = '['
RRANGE = ']'
COLON = ':'

# Define module item types
PARAMETER = 'parameter'
INPUT = 'input'
OUTPUT = 'output'
INOUT = 'inout'
NET = 'net'
REG = 'reg'
INTEGER = 'integer'
REAL = 'real'
TIME = 'time'
EVENT = 'event'
GATE_INSTANTIATION = 'gate_instantiation'
UDP_INSTANTIATION = 'udp_instantiation'
MODULE_INSTANTIATION = 'module_instantiation'
INITIAL_STATEMENT = 'initial_statement'
ALWAYS_STATEMENT = 'always_statement'
TASK = 'task'
FUNCTION = 'function'
ENDFUNCTION = 'endfunction'

WIRE = 'wire'
ASSIGN = 'assign'
IF = 'if'
ELSE = 'else'
WHILE = 'while'
FOR = 'for'
BEGIN = 'begin'
END = 'end'
CASE = 'case'
ENDCASE = 'endcase'
DEFAULT = 'default'
OPERATOR = ''
COMMA = ','
LPAREN = '('
RPAREN = ')'
LBRACE = '{'
RBRACE = '}'
EQUALS = '='
INT = 'int'

# regex for various kind of tokens
TOKENS = [
    (MODULE, r'module'),
    (ENDMODULE, r'endmodule'),
    (INPUT, r'input'),
    (OUTPUT, r'output'),
    (WIRE, r'wire'),
    (REG, r'reg'),
    (ASSIGN, r'assign'),
    (IF, r'if'),
    (ELSE, r'else'),
    (WHILE, r'while'),
    (FOR, r'for'),
    (BEGIN, r'begin'),
    (END, r'end'),
    (CASE, r'case'),
    (ENDCASE, r'endcase'),
    (DEFAULT, r'default'),
    (FUNCTION, r'function'),
    (ENDFUNCTION, r'endfunction'),
    (INTEGER, r'integer'),
    (REAL, r'real'),
    (TIME, r'time')
    (INT, r'\d+'),
    (IDENTIFIER, r'[a-zA-Z_][a-zA-Z0-9_$]*'),
    (OPERATOR, r'[+\-*/%]'),
    (LPAREN, r'\('),
    (RPAREN, r'\)'),
    (LBRACE, r'\{'),
    (RBRACE, r'\}'),
    (COMMA, r','),
    (SEMICOLON, r';'),
    (COLON, r':'),
    (LRANGE, r'\['),
    (RRANGE, r'\]'),
    (None, None),
    (EQUALS, r'=')
]
