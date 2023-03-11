from tokens import *
from constants import *


def is_symbol(char):
    '''
    Function to check if a character is a symbol
    '''
    return char in SYMBOLS


def is_operator(char):
    '''
    Function to check if a character is an operator
    '''
    return char in OPERATORS


def is_keyword(string):
    '''
    Function to check if a string is a keyword
    '''
    return string in KEYWORDS
