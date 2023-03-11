from tokens import *
from lexical_analyser import *


class VerilogSyntaxAnalyser:
    '''
    Define the parse functions for each construct
    '''

    def __init__(self, code):
        self.lexer = VerilogLexer(code)

    def parse_module_declaration(self):
        if self.lexer.get_next_token().token_type != MODULE:
            raise ValueError('Expected "module" keyword')

        identifier = self.lexer.get_next_token()

        if identifier.value[0].isnumeric():
            raise ValueError('Module identifier must not start with a number')

        port_list = self.parse_port_list()

        if self.lexer.get_current_token().token_type != SEMICOLON:
            raise ValueError('Expected ";" after module declaration')

    def parse_data_type(self):
        # signed data type not included
        data_type = ''
        dimensions = []
        if self.lexer.get_current_token().token_type in [REAL, TIME, INTEGER]:
            data_type = self.lexer.get_current_token().value
            self.lexer.get_next_token()
        elif self.lexer.get_current_token().token_type in [REG, WIRE]:
            data_type = self.lexer.get_current_token().value
            if self.lexer.get_next_token().token_type == LRANGE:
                dimensions.append(self.parse_expression())
                if self.lexer.get_current_token().token_type != RRANGE:
                    raise ValueError('Expected "]" after array dimension')
                self.lexer.get_next_token()
        elif self.lexer.get_current_token().token_type == LRANGE:
            dimensions.append(self.parse_expression())
            if self.lexer.get_current_token().token_type != RRANGE:
                raise ValueError('Expected "]" after array dimension')
            self.lexer.get_next_token()
        else:
            return None

        data_type_obj = {
            'name': data_type,
            'dimensions': dimensions,
        }

        return data_type_obj

    def parse_port_list(self):
        if self.lexer.get_next_token().token_type == SEMICOLON:
            return

        if self.lexer.get_current_token().token_type != LPAREN:
            raise ValueError('Expected "(" in port list')

        ports = []
        token = None

        while True:
            token = self.lexer.get_next_token()
            if token.token_type is None:
                raise ValueError('Unexpected end of input in port list')
            elif token.token_type == RPAREN:
                break
            else:
                direction = None

                port_name = self.parse_in_out_declaration()
                # if token.token_type in [INPUT, OUTPUT, INOUT]:
                #     direction = token.token_type
                #     token = self.lexer.get_next_token().token_type
                #     # self.lexer.get_next_token()
                #     # print(self.lexer.get_current_token().value)
                #     data_type = self.parse_data_type()
                #     # print(data_type)
                #     # if self.lexer.get_current_token() == '[':
                #     #     port_size = self.parse_expression()
                #     #     if self.lexer.get_next_token() != ']':
                #     #         raise ValueError('Expected "]" after port size')
                #     #     data_type = {'type': 'array',
                #     #                  'base_type': data_type, 'size': port_size}

                # if self.lexer.get_current_token().token_type != IDENTIFIER:
                #     raise ValueError('Expected port identifier')
                # port_name = self.lexer.get_current_token().value
                # ports.append(
                #     {'name': port_name, 'direction': direction, 'data_type': data_type})

                if self.lexer.get_next_token().token_type == COMMA:
                    continue
                elif self.lexer.get_current_token().token_type == RPAREN:
                    break
                else:
                    raise ValueError('Expected "," or ")" in port list')

        if self.lexer.get_current_token().token_type != RPAREN:
            raise ValueError('Expected ")" after port list')

        self.lexer.get_next_token()

        return ports

    def parse_parameter_declaration(self):
        parameter_names = []
        parameter_values = []

        while True:
            if self.lexer.get_next_token().token_type != IDENTIFIER:
                raise ValueError('Expected parameter name')
            parameter_names.append(self.lexer.get_current_token().value)

            if self.lexer.get_next_token().token_type != EQUALS:
                raise ValueError('Expected "=" in parameter declaration')

            if self.lexer.get_next_token().token_type != IDENTIFIER:
                raise ValueError('Expected parameter name')
            parameter_values.append(self.lexer.get_current_token().value)

            if self.lexer.get_next_token().token_type == COMMA:
                continue
            elif self.lexer.get_current_token().token_type == SEMICOLON:
                break
            else:
                raise ValueError('Expected comma or semicolon')

        return {'names': parameter_names, 'values': parameter_values}

    def parse_expression(self):
        dimensions = []
        token = self.lexer.get_next_token()
        if token.token_type != INT and token.token_type != IDENTIFIER:
            raise ValueError('Incorrect values')
        dimensions.append(token.value)
        token = self.lexer.get_next_token()
        if token.token_type == OPERATOR:
            dimensions.append(token.value)
            token = self.lexer.get_next_token()
            if token.token_type != INT and token.token_type != IDENTIFIER:
                raise ValueError('Incorrect values')
            dimensions.append(token.value)
            self.lexer.get_next_token()
        if self.lexer.get_current_token().token_type != COLON:
            raise ValueError('Expected :')
        dimensions.append(self.lexer.get_current_token().value)
        token = self.lexer.get_next_token()
        if token.token_type != INT and token.token_type != IDENTIFIER:
            raise ValueError('Incorrect values')
        dimensions.append(self.lexer.get_current_token().value)
        self.lexer.get_next_token()
        return dimensions

    def parse_in_out_declaration(self):
        self.lexer.get_next_token()
        data_type = self.parse_data_type()
        port_name = self.parse_identifier()

        return port_name

    def parse_identifier(self):
        if self.lexer.get_current_token().token_type != IDENTIFIER:
            raise ValueError('Expected variable identifier')
        identifier = self.lexer.get_current_token().value

        return identifier

    def parse_identifier_declaration(self):
        identifier = self.lexer.get_current_token().value

        expression = []

        if self.lexer.get_next_token().token_type == EQUALS:        
            expression = self.parse_complex_num_expression()
            
        if self.lexer.get_current_token().token_type != SEMICOLON:
            raise ValueError('Expected ";" after identifier declaration')

        return {identifier, expression}
    
    def parse_complex_num_expression(self):
        expression = []
        token = self.lexer.get_next_token()
        lparam_count = 0
        while not (token.token_type == NEWLINE or token.token_type== SEMICOLON):
            if token.token_type == IDENTIFIER or token.token_type == INT or token.token_type == STRING:
                if self.lexer.last_token.token_type in [RPAREN, IDENTIFIER, INT, STRING]:
                    raise ValueError(f'Invalid expression - " {self.lexer.last_token.value} {token.value} " ')
            if token.token_type == LPAREN:
                if self.lexer.last_token.token_type not in [OPERATOR, LSHIFT, RSHIFT, EQUALS]:
                    raise ValueError('Invalid expression, no operator before paranthesis')
                lparam_count += 1
            if token.token_type in [OPERATOR, LSHIFT, RSHIFT]:
                if self.lexer.last_token.token_type in [LPAREN, OPERATOR, LSHIFT, RSHIFT, EQUALS] :
                    raise ValueError('Invalid expression, operator not valid here')
            if token.token_type == RPAREN:
                if lparam_count <=0:
                    raise ValueError('Invalid expression, no opening paranthesis')
                lparam_count -= 1
                if self.lexer.last_token.token_type in [OPERATOR, LSHIFT, RSHIFT, EQUALS]:
                    raise ValueError('Invalid expression, operator before paranthesis')
                
            expression.append(token.value)
            token = self.lexer.get_next_token()

        if lparam_count != 0:
            raise ValueError('Expected closing bracket')
        
        if token.token_type == NEWLINE:
            raise ValueError('Semicolon expected at the end of expression')

        return expression
    
    def parse_time_declaration(self):
        pass

    def parse_event_declaration(self):
        pass

    def parse_gate_instantiation(self):
        pass

    def parse_udp_instantiation(self):
        pass

    def parse_module_instantiation(self):
        pass

    def parse_initial_statement(self):
        pass

    def parse_always_statement(self):
        pass

    def parse_task_declaration(self):
        pass

    def parse_net_declaration(self):
        data_type = self.parse_data_type()
        id = self.parse_identifier()
        if self.lexer.get_next_token().token_type != SEMICOLON:
            raise ValueError('Expected ";" after wire declaration')

        return

    def parse_reg_declaration(self):
        data_type = self.parse_data_type()
        id = self.parse_identifier()
        if self.lexer.get_next_token().token_type == EQUALS:
            if self.lexer.get_next_token().token_type != STRING:
                raise ValueError('Expected string')
            self.lexer.get_next_token()
        if self.lexer.get_current_token().token_type != SEMICOLON:
            raise ValueError('Expected ";" after reg declaration')

        return

    def parse_function_declaration(self):
        self.lexer.get_next_token()
        return_type = self.parse_data_type()

        token = self.lexer.get_current_token()
        if token.token_type != IDENTIFIER:
            raise ValueError('Expected function identifier')
        function_name = token.value

        port_list = self.parse_port_list()

        if self.lexer.get_next_token().token_type != SEMICOLON:
            raise ValueError('Expected ";" after function declaration')

        function_body = []

        while True:
            # sahi nhi
            token = self.lexer.get_next_token()
            if token is None:
                raise ValueError('Unexpected end of input')
            elif token == ENDFUNCTION:
                break
            else:
                function_body.append(token)

    def parse_verilog_code(self):
        module_declaration = self.parse_module_declaration()
        module_items = []
        while True:
            token = self.lexer.get_next_token().token_type
            if token is None:
                raise ValueError('Unexpected end of input')
            elif token == MODULE:
                raise ValueError('Unexpected module declaration')
                break
            elif token == ENDMODULE:
                break
            elif token == NEWLINE:
                continue
            elif token == PARAMETER:
                module_items.append(self.parse_parameter_declaration())
            elif token == INPUT or token == OUTPUT or token == INOUT:
                module_items.append(self.parse_in_out_declaration())
                if self.lexer.get_next_token().token_type != SEMICOLON:
                    raise ValueError(f'Expected ";" after {token} declaration')
            elif token == WIRE:
                module_items.append(self.parse_net_declaration())
            elif token == REG:
                module_items.append(self.parse_reg_declaration())
            elif token == INTEGER or token == REAL or token == TIME:
                data_type = self.parse_data_type()
                id = self.parse_identifier_declaration()
                # module_items.append(self.parse_net_or_variables_declaration())
            elif token == ASSIGN:
                module_items.append(self.parse_assign_expression())
            elif token == EVENT:
                module_items.append(self.parse_event_declaration())
            elif token == GATE_INSTANTIATION:
                module_items.append(self.parse_gate_instantiation())
            elif token == UDP_INSTANTIATION:
                module_items.append(self.parse_udp_instantiation())
            elif token == MODULE_INSTANTIATION:
                module_items.append(self.parse_module_instantiation())
            elif token == INITIAL_STATEMENT:
                module_items.append(self.parse_initial_statement())
            elif token == ALWAYS_STATEMENT:
                module_items.append(self.parse_always_statement())
            elif token == TASK:
                module_items.append(self.parse_task_declaration())
            elif token == FUNCTION:
                module_items.append(self.parse_function_declaration())
            elif token == IDENTIFIER:
                module_items.append(self.parse_identifier_declaration())
            else:
                raise ValueError(
                    f'Unexpected token "{token}" in module declaration')
        # modules.append({'identifier': identifier, 'port_list': port_list, 'items': module_items})


f = open("demofile.vlg", "r")
lex_obj = VerilogSyntaxAnalyser(f.read())
lex_obj.parse_verilog_code()
# sl = VerilogSyntaxAnalyser()
