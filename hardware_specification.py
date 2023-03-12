import re
from tokens import *


class HardwareSpecification:
    '''
    Class to represent a hardware specification
    '''

    def __init__(self):
        self.type_dict = {}
        self.direction_dict = {}

    def add_hardware(self, value, type, direction):
        if self.type_dict.get(value) == None or type is None:
            if self.direction_dict.get(value) == None or direction is None:
                if direction:
                    self.direction_dict[value] = (direction)
                if type:
                    self.type_dict[value] = (type)
                return {'error': False}
            else:
                return{'error': True, 'reason': f'Direction already declared for identifier {value}'}
        else:
            return{'error': True, 'reason': f'Type already declared for identifier {value}'}
