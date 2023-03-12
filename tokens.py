'''
Define Verilog tokens and module item types
'''

# token types
MODULE = 'module'
ENDMODULE = 'endmodule'
IDENTIFIER = 'identifier'
PORT = 'port'
SEMICOLON = 'semicolon'
LRANGE = 'left_range_bracket'
RRANGE = 'right_range_bracket'
COLON = 'colon'

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

#symbols, operators and delimiters
OPERATOR = 'ops'
COMMA = 'comma'
LPAREN = 'left_paranthesis'
RPAREN = 'right_paranthesis'
LBRACE = 'left_brace'
RBRACE = 'right_brace'
EQUALS = 'equal_to'
INT = 'int'
EOF = 'eof'
STRING = 'str'
INVALID = 'inv'
DISPLAY = '$display'
LSHIFT = 'left_shift'
RSHIFT = 'right_shift'
NEWLINE = '\n'
BOOL_OP = 'bop'
ADV_TIME = 'adt'

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
    (TIME, r'time'),
    (DISPLAY, r'\$display'),
    (INT, r'-?\d+'),
    (INT, r'-?0x[\d]+'),
    (INT, r'-?\d*\'b[0-1]*'),
    (INT, r'-?\d*\'[oO][0-7]*'),
    (INT, r'-?\d*\'[hH][0-9a-fA-F][0-9a-fA-F_]*'),
    (INT, r'-?\d*\'[dD][0-9]*'),
    (IDENTIFIER, r'[a-zA-Z_][a-zA-Z0-9_$]*'),
    (OPERATOR, r'[+\-*/%]'),
    (BOOL_OP, r'[~&\|^]'),
    (ADV_TIME, r'#[\d]+'),
    (LPAREN, r'\('),
    (RPAREN, r'\)'),
    (LBRACE, r'\{'),
    (RBRACE, r'\}'),
    (COMMA, r','),
    (SEMICOLON, r';'),
    (COLON, r':'),
    (LRANGE, r'\['),
    (RRANGE, r'\]'),
    (EQUALS, r'='),
    (STRING, r'\".*\"'),
    (LSHIFT, r'<<'),
    (RSHIFT, r'>>'),
    (NEWLINE, r'\n'),
    (INVALID, r'.*'),
    (None, None),
]
