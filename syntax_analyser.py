from tokens import *
from hardware_specification import *
from lexical_analyser import *


class VerilogSyntaxAnalyser:
    '''
    Define the parse functions for each construct
    '''

    def __init__(self, code):
        self.lexer = VerilogLexer(code)
        self.line_num = 1
        self.error = False
        self.errors = []
        self.hware_specifications = HardwareSpecification()
        self.modules = set()
        self.module_functions = {}
        self.current_module = None
        self.eof = False

    def raise_error(self, error):
        self.error = True
        self.errors.append({
            'line_num': self.line_num,
            'error': error,
        })
        token = self.lexer.get_next_token()
        while token.token_type not in [NEWLINE, EOF]:
            token = self.lexer.get_next_token()
        return

    def parse_module_declaration(self):
        if self.error:
            return

        while self.lexer.get_next_token().token_type == NEWLINE:
            self.line_num +=1

        if self.lexer.get_current_token().token_type == EOF :
            self.eof = True
            return

        if self.lexer.get_current_token().token_type != MODULE:
            self.raise_error('Expected "module" keyword')
            return

        if self.lexer.get_next_token().token_type != IDENTIFIER:
            self.raise_error('Expected module identifier')
            return

        self.current_module = self.lexer.get_current_token().value

        self.parse_port_list()
        if self.error:
            return

        if self.lexer.get_current_token().token_type != SEMICOLON:
            self.raise_error('Expected ";" after module declaration')
            return

    def parse_data_type(self):
        if self.error:
            return
        # signed data type not included
        data_type = ''
        dimensions = []
        if self.lexer.get_current_token().token_type in [REAL, TIME, INTEGER]:
            data_type = self.lexer.get_current_token().value
            self.lexer.get_next_token()
            return data_type
        elif self.lexer.get_current_token().token_type in [REG, WIRE]:
            data_type = self.lexer.get_current_token().value
            if self.lexer.get_next_token().token_type == LRANGE:
                dimensions = self.parse_expression()
                if self.error:
                    return
                if self.lexer.get_current_token().token_type != RRANGE:
                    self.raise_error('Expected "]" after array dimension')
                    return
                self.lexer.get_next_token()
            return data_type
        elif self.lexer.get_current_token().token_type == LRANGE:
            dimesions = self.parse_expression()
            if self.error:
                return
            if self.lexer.get_current_token().token_type != RRANGE:
                self.raise_error('Expected "]" after array dimension')
                return
            self.lexer.get_next_token()
            return None
        else:
            return

    def parse_port_list(self):
        if self.error:
            return
        if self.lexer.get_next_token().token_type == SEMICOLON:
            return

        if self.lexer.get_current_token().token_type != LPAREN:
            self.raise_error('Expected "(" in port list')
            return

        ports = []
        token = None

        while True:
            token = self.lexer.get_next_token()
            if token.token_type is None:
                self.raise_error('Unexpected end of input in port list')
                return
            elif token.token_type == RPAREN:
                break
            else:
                None

                self.parse_in_out_declaration()
                if self.error:
                    return

                if self.lexer.get_next_token().token_type == COMMA:
                    continue
                elif self.lexer.get_current_token().token_type == RPAREN:
                    break
                else:
                    self.raise_error('Expected "," or ")" in port list')
                    return

        if self.lexer.get_current_token().token_type != RPAREN:
            self.raise_error('Expected ")" after port list')
            return

        self.lexer.get_next_token()

        return

    def parse_parameter_declaration(self):
        if self.error:
            return
        parameter_names = []
        parameter_values = []

        while True:
            if self.lexer.get_next_token().token_type != IDENTIFIER:
                self.raise_error('Expected parameter name')
                return
            parameter_names.append(self.lexer.get_current_token().value)

            if self.lexer.get_next_token().token_type != EQUALS:
                self.raise_error('Expected "=" in parameter declaration')
                return

            if self.lexer.get_next_token().token_type != IDENTIFIER:
                self.raise_error('Expected parameter name')
                return
            parameter_values.append(self.lexer.get_current_token().value)

            if self.lexer.get_next_token().token_type == COMMA:
                continue
            elif self.lexer.get_current_token().token_type == SEMICOLON:
                break
            else:
                self.raise_error('Expected comma or semicolon')
                return

    def parse_expression(self):
        if self.error:
            return
        dimensions = []
        token = self.lexer.get_next_token()
        if token.token_type != INT and token.token_type != IDENTIFIER:
            self.raise_error('Incorrect values')
            return
        dimensions.append(token.value)
        token = self.lexer.get_next_token()
        if token.token_type == OPERATOR:
            dimensions.append(token.value)
            token = self.lexer.get_next_token()
            if token.token_type != INT and token.token_type != IDENTIFIER:
                self.raise_error('Incorrect values')
                return
            dimensions.append(token.value)
            self.lexer.get_next_token()
        if self.lexer.get_current_token().token_type != COLON:
            self.raise_error('Expected : in range')
            return
        dimensions.append(self.lexer.get_current_token().value)
        token = self.lexer.get_next_token()
        if token.token_type != INT and token.token_type != IDENTIFIER:
            self.raise_error('Incorrect values')
            return
        dimensions.append(self.lexer.get_current_token().value)
        self.lexer.get_next_token()
        return dimensions

    def parse_in_out_declaration(self):
        if self.error:
            return
        direction = self.lexer.get_current_token().value
        self.lexer.get_next_token()
        data_type = self.parse_data_type()
        identifier = self.parse_identifier()
        if self.error:
            return
        if data_type in [REAL, TIME, INTEGER]:
            self.raise_error(
                'real, time, Integer data types not declared with input, output or inout')
            return

        result = self.hware_specifications.add_hardware(
            identifier, data_type, direction)
        if result['error']:
            self.raise_error(result['reason'])
            return

        return

    def parse_identifier(self):
        if self.error:
            return
        if self.lexer.get_current_token().token_type != IDENTIFIER:
            self.raise_error('Expected variable identifier')
            return
        identifier = self.lexer.get_current_token().value

        return identifier

    def parse_identifier_declaration(self):
        if self.error:
            return
        identifier = self.lexer.get_current_token().value

        if self.lexer.get_next_token().token_type == EQUALS:
            token = self.lexer.get_next_token()
            if token.token_type in [AND, OR, XOR]:
                self.parse_basic_gates(2)
            elif token.token_type in [NOT]:
                self.parse_basic_gates(1)
            else:
                self.parse_complex_num_expression()
            if self.error:
                return
        if self.lexer.get_current_token().token_type != SEMICOLON:
            self.raise_error('Expected ";" after identifier declaration')
            return

        return

    def parse_complex_num_expression(self):
        if self.error:
            return
        expression = []
        token = self.lexer.get_current_token()
        lparam_count = 0
        while not (token.token_type == NEWLINE or token.token_type == SEMICOLON):
            if token.token_type == IDENTIFIER or token.token_type == INT or token.token_type == STRING:
                if self.lexer.last_token.token_type in [RPAREN, IDENTIFIER, INT, STRING]:
                    self.raise_error(
                        f'Invalid expression - " {self.lexer.last_token.value} {token.value} " ')
                    return
            elif token.token_type == LPAREN:
                if self.lexer.last_token.token_type not in [OPERATOR, LSHIFT, RSHIFT, EQUALS]:
                    self.raise_error(
                        'Invalid expression, no operator before paranthesis')
                    return
                lparam_count += 1
            elif token.token_type in [OPERATOR, LSHIFT, RSHIFT]:
                if self.lexer.last_token.token_type in [LPAREN, OPERATOR, LSHIFT, RSHIFT, EQUALS]:
                    self.raise_error(
                        'Invalid expression, operator not valid here')
                    return
            elif token.token_type == RPAREN:
                if lparam_count <= 0:
                    self.raise_error(
                        'Invalid expression, no opening paranthesis')
                    return
                lparam_count -= 1
                if self.lexer.last_token.token_type in [OPERATOR, LSHIFT, RSHIFT, EQUALS]:
                    self.raise_error(
                        'Invalid expression, operator before paranthesis')
                    return
            else:
                self.raise_error('Invalid token found in expression')
                return

            expression.append(token.value)
            token = self.lexer.get_next_token()

        if lparam_count != 0:
            self.raise_error('Expected closing bracket')
            return

        if token.token_type == NEWLINE:
            self.raise_error('Semicolon expected at the end of expression')
            return

        return

    def parse_event_declaration(self):
        if self.error:
            return
        pass

    def parse_gate_instantiation(self):
        if self.error:
            return
        pass

    def parse_udp_instantiation(self):
        if self.error:
            return
        pass

    def parse_module_instantiation(self):
        if self.error:
            return
        pass

    def parse_initial_statement(self):
        if self.error:
            return
        pass

    def parse_always_statement(self):
        if self.error:
            return
        pass

    def parse_task_declaration(self):
        if self.error:
            return
        pass

    def parse_display_declarartion(self):
        if self.lexer.get_next_token().token_type != LPAREN:
            self.raise_error('Expected "(" after $display declaration')
            return
        while self.lexer.get_current_token().token_type != RPAREN:
            if self.lexer.get_next_token().token_type not in [STRING, IDENTIFIER]:
                self.raise_error(
                    'Expected string or identifier in $display declaration')
                return
            if self.lexer.get_next_token().token_type == COMMA:
                continue
            elif self.lexer.get_current_token().token_type != RPAREN:
                self.raise_error(
                    f'Expected \',\' or \')\' in $display declaration after {self.lexer.last_token.value}')
                return
        if self.lexer.get_next_token().token_type != SEMICOLON:
            self.raise_error(
                'Expected ; after $display declaration')
            return

    def parse_net_declaration(self):
        if self.error:
            return
        self.parse_data_type()
        identifier = self.parse_identifier()
        if self.error:
            return

        result = self.hware_specifications.add_hardware(identifier, WIRE, None)
        if result['error']:
            self.raise_error(result['reason'])
            return

        if self.lexer.get_next_token().token_type != SEMICOLON:
            self.raise_error('Expected ";" after wire declaration')
            return

        return

    def parse_reg_declaration(self):
        if self.error:
            return
        self.parse_data_type()
        identifier = self.parse_identifier()

        result = self.hware_specifications.add_hardware(identifier, REG, None)
        if result['error']:
            self.raise_error(result['reason'])
            return

        if self.error:
            return
        if self.lexer.get_next_token().token_type == EQUALS:
            if self.lexer.get_next_token().token_type != STRING:
                self.raise_error('Expected string')
                return
            self.lexer.get_next_token()
        if self.lexer.get_current_token().token_type != SEMICOLON:
            self.raise_error('Expected ";" after reg declaration')
            return

        return

    def parse_assign_declaration(self):
        if self.error:
            return
        identifier = self.lexer.get_next_token().value

        expression = []

        if self.lexer.get_next_token().token_type == EQUALS:
            self.parse_assign_expression()
            if self.error:
                return

        if self.lexer.get_current_token().token_type != SEMICOLON:
            self.raise_error('Expected ";" after identifier declaration')
            return

        return

    def parse_assign_expression(self):
        if self.error:
            return
        expression = []
        token = self.lexer.get_next_token()
        lparam_count = 0
        while not (token.token_type == NEWLINE or token.token_type == SEMICOLON):
            if token.token_type == IDENTIFIER:
                if self.lexer.last_token.token_type in [RPAREN, IDENTIFIER]:
                    self.raise_error(
                        f'Invalid expression - " {self.lexer.last_token.value} {token.value} " ')
                    return
            elif token.token_type == LPAREN:
                if self.lexer.last_token.token_type not in [BOOL_OP, EQUALS]:
                    self.raise_error(
                        'Invalid expression, no operator before paranthesis')
                    return
                lparam_count += 1
            elif token.token_type == BOOL_OP:
                if self.lexer.last_token.token_type in [LPAREN, BOOL_OP, EQUALS]:
                    self.raise_error(
                        'Invalid expression, operator not valid here')
                    return
            elif token.token_type == RPAREN:
                if lparam_count <= 0:
                    self.raise_error(
                        'Invalid expression, no opening paranthesis')
                    return
                lparam_count -= 1
                if self.lexer.last_token.token_type in [BOOL_OP, EQUALS]:
                    self.raise_error(
                        'Invalid expression, operator before paranthesis')
                    return
            else:
                self.raise_error('Invalid token found in expression')
                return

            expression.append(token.value)
            token = self.lexer.get_next_token()

        if lparam_count != 0:
            self.raise_error('Expected closing bracket')
            return

        if token.token_type == NEWLINE:
            self.raise_error('Semicolon expected at the end of expression')
            return

        return

    def parse_function_declaration(self):
        if self.error:
            return
        self.lexer.get_next_token()
        self.parse_data_type()
        if self.error:
            return

        token = self.lexer.get_current_token()
        if token.token_type != IDENTIFIER:
            self.raise_error('Expected function identifier')
            return
        function_name = token.value

        if self.module_functions.get(self.current_module) == None:
            self.module_functions[self.current_module] = []
        self.module_functions[self.current_module].append(function_name)
        # print(self.module_functions[self.current_module])
        # print(function_name)

        self.parse_port_list()
        if self.error:
            return

        if self.lexer.get_current_token().token_type != SEMICOLON:
            self.raise_error('Expected ";" after function declaration')
            return

        function_body = []

        while True:
            # improvise
            token = self.lexer.get_next_token()
            if token is None:
                self.raise_error('Unexpected end of input')
                return
            elif token.token_type == NEWLINE:
                self.line_num += 1
            elif token.token_type == ENDFUNCTION:
                break
            else:
                function_body.append(token)

    def parse_basic_gates(self, inp):
        gate_type = self.lexer.get_current_token().token_type
        var = inp+1
        if self.lexer.get_next_token().token_type != LPAREN:
            self.raise_error('Expected \'(\' after gate declaration')
            return
        while var > 0:
            if self.lexer.get_next_token().token_type != IDENTIFIER:
                self.raise_error('Expected identifier in gate declaration')
                return
            var -= 1
            token = self.lexer.get_next_token()
            if var > 0 and token.token_type != COMMA:
                self.raise_error(
                    'Expected , after identifier in gate declaration')
                return
            if var == 0 and token.token_type != RPAREN:
                self.raise_error(
                    'Expected ) after identifier in gate declaration')
                return
        if self.lexer.get_next_token().token_type != SEMICOLON:
            self.raise_error('Expected ; after gate declaration')
            return

    def parse_module_body(self):
        if self.lexer.get_current_token().token_type == EOF:
            self.eof = True
            return
        while True:
            token = self.lexer.get_next_token().token_type
            if token is None:
                self.raise_error('Unexpected end of input')
            elif token == MODULE:
                self.raise_error('Unexpected module declaration')
            elif token == ENDMODULE:
                break
            elif token == NEWLINE:
                self.error = False
                self.line_num += 1
                continue
            elif token == PARAMETER:
                self.parse_parameter_declaration()
            elif token == INPUT or token == OUTPUT or token == INOUT:
                self.parse_in_out_declaration()
                if self.error:
                    self.error = False
                    self.line_num += 1
                    continue
                if self.lexer.get_next_token().token_type != SEMICOLON:
                    self.raise_error(f'Expected ";" after {token} declaration')
            elif token == WIRE:
                self.parse_net_declaration()
            elif token == REG:
                self.parse_reg_declaration()
            elif token == INTEGER or token == REAL or token == TIME:
                data_type = self.parse_data_type()
                id = self.parse_identifier_declaration()
            elif token == ASSIGN:
                self.parse_assign_declaration()
            elif token == DISPLAY:
                self.parse_display_declarartion()
            elif token == AND or token == XOR or token == OR:
                self.parse_basic_gates(2)
            elif token == NOT:
                self.parse_basic_gates(1)
            elif token == EVENT:
                self.parse_event_declaration()
            elif token == GATE_INSTANTIATION:
                self.parse_gate_instantiation()
            elif token == UDP_INSTANTIATION:
                self.parse_udp_instantiation()
            elif token == MODULE_INSTANTIATION:
                self.parse_module_instantiation()
            elif token == INITIAL_STATEMENT:
                self.parse_initial_statement()
            elif token == ALWAYS_STATEMENT:
                self.parse_always_statement()
            elif token == TASK:
                self.parse_task_declaration()
            elif token == FUNCTION:
                self.parse_function_declaration()
            elif token == IDENTIFIER:
                self.parse_identifier_declaration()
            elif token == EOF:
                self.eof = True
                break
            else:
                self.raise_error(
                    f'Unexpected token "{token}" in module declaration')
            if self.lexer.get_current_token().token_type == NEWLINE:
                self.error = False
                self.line_num += 1
                continue

    def parse_verilog_code(self):
        while not self.eof:
            module_declaration = self.parse_module_declaration()
            if self.eof:
                break
            module_body = self.parse_module_body()
            if self.lexer.get_current_token().token_type == EOF:
                break
        return self.errors, self.hware_specifications
