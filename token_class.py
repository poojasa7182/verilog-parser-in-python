import re
from tokens import *


class Token:
    '''
    Class to represent a token
    '''

    def __init__(self, value):
        self.value = value

        if value == None:
            self.token_type = EOF
            return

        match = None
        for token_type, pattern in TOKENS:
            regex = re.compile(pattern)
            match = regex.match(value)
            if match:
                value = match.group(0)
                self.token_type = token_type
                break
        if not match:
            raise SyntaxError('Invalid syntax')
