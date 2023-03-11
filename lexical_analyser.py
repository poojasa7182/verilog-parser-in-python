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
        self.comments = []
        self.errors = []
        self.line_num = 1
        # self.tokens = []

    def get_next_token(self):

        if self.current_token != None:
            self.last_token = self.current_token

        while self.pos < len(self.code) and self.code[self.pos] in WHITESPACE:
            if self.code[self.pos] == '\n':
                self.current_token = Token('\n')
                self.line_num += 1
                self.pos += 1
                return self.current_token
            self.pos += 1

        if self.pos >= len(self.code):
            self.current_token = Token(None)
            return self.current_token

        if self.code[self.pos] == "\"":
            value = "\""
            self.pos += 1
            while self.code[self.pos] != "\"":
                value += self.code[self.pos]
                self.pos += 1
                if self.code[self.pos] == '\n':
                    self.errors.append(
                        {self.line_num, "Illegal for a string to be split into two lines"})
                    break

            if self.code[self.pos] == "\"":
                value += self.code[self.pos]
                self.pos += 1
            self.current_token = Token(value)
            return self.current_token
            
        elif self.code[self.pos] == "/" and self.code[self.pos] == self.code[self.pos+1]:
            value = ""
            while self.code[self.pos] != "\n":
                value += self.code[self.pos]
                self.pos += 1
            self.comments.append(value[2:])
            return self.get_next_token()
        
        elif self.code[self.pos] == "/" and self.code[self.pos+1] == "*":
            value = ""
            while not (self.code[self.pos] == "*" and self.code[self.pos+1] == "/"):
                value += self.code[self.pos]
                if self.code[self.pos] == '\n':
                    self.line_num += 1
                self.pos += 1
                if self.pos == len(self.code):
                    self.errors.append(
                        {self.line_num+1, "Non terminating comment"})
                    return self.get_next_token()
            self.comments.append(value[2:])
            self.pos += 2
            return self.get_next_token()

        if self.code[self.pos] in DELIMITERS or self.code[self.pos] in OPERATORS:
            value = self.code[self.pos]
            self.pos += 1
            if self.code[self.pos] == '<' and self.code[self.pos-1] == '<':
                value += self.code[self.pos]
                self.pos += 1
            if self.code[self.pos] == '>' and self.code[self.pos-1] == '>':
                value += self.code[self.pos]
                self.pos += 1
            
            self.current_token = Token(value)
            return self.current_token

        value = ""
        while self.code[self.pos] not in DELIMITERS and self.code[self.pos] not in OPERATORS:
            value += self.code[self.pos]
            self.pos += 1
            if self.pos == len(self.code):
                break
        self.current_token = Token(value)
        if self.current_token.token_type == INVALID:
            self.errors.append(
                {self.line_num, f"Invalid token {self.current_token.value}"})
        return self.current_token

    def get_current_token(self):
        return self.current_token
