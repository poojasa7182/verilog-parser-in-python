'''
Define constants in used in Verilog code 
'''


WHITESPACE = ' \t\n\r'

DELIMITERS = [' ',
              '\n',
              '\t',
              '(',
              ')',
              '[',
              ']',
              '{',
              '}',
              ':',
              ';',
              ',',
              '=',
              '<',
              '>',
            ]

SYMBOLS = '!@#$%^&*()_-+={}[]|\:;"<>,.?/~`'

OPERATORS = ['+',
             '-',
             '*',
             '/',
             '%',
             '&',
             '|',
             '^',
             '~',
             '<<',
             '>>'
             ]

KEYWORDS = ['module',
            'endmodule',
            'input',
            'output',
            'wire',
            'reg',
            'assign',
            'always',
            'if',
            'else',
            'while',
            'for',
            'begin',
            'end',
            'integer',
            'case',
            'endcase',
            'default',
            'function'
            ]
