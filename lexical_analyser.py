from tokens import *
from token_class import *
from helper_functions import *
from constants import *


class VerilogLexer:
    '''
    Class to represent the Verilog Lexer
    '''

    def __init__(self, code):
        self.code = code
        self.pos = 0
        self.last_token = None
        self.current_token = None

    def get_next_token(self):

        if self.current_token != None :
            self.last_token = self.current_token

        while self.pos < len(self.code) and self.code[self.pos] in WHITESPACE:
            self.pos += 1

        if self.pos == len(self.code):
            self.current_token = Token(None)
            return self.current_token

        if self.code[self.pos].isdigit():
            value = ''
            while self.pos < len(self.code) and self.code[self.pos].isdigit():
                value += self.code[self.pos]
                self.pos += 1
            self.current_token = Token(value)
            return self.current_token

        if self.code[self.pos].isalpha() or self.code[self.pos] == '_':
            value = ''
            while self.pos < len(self.code) and (self.code[self.pos].isalnum() or self.code[self.pos] == '_'):
                value += self.code[self.pos]
                self.pos += 1
            if is_keyword(value):
                self.current_token = Token(value)
                return self.current_token
            else:
                self.current_token = Token(value)
                return self.current_token

        if is_symbol(self.code[self.pos]):
            value = ''
            while self.pos < len(self.code) and is_symbol(self.code[self.pos]):
                value += self.code[self.pos]
                self.pos += 1
            self.current_token = Token(value)
            return self.current_token
        
    def get_current_token(self):
        return self.current_token
