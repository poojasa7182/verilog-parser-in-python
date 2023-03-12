from lexical_analyser import *
from syntax_analyser import *
from hardware_specification import *


class VerilogParser:
    '''
    Class to represent Verilog Parser
    '''

    def __init__(self, code):
        self.lexer = VerilogLexer(code)
        self.parser = VerilogSyntaxAnalyser(code)

    def tokenize(self):
        file_tokens = open("symbol_table.txt", "w")
        file_tokens.write('LEXEME\t\t\tTOKEN TYPE\n\n')
        while True:
            token = self.lexer.get_next_token()
            if token.token_type is EOF:
                break
            if token.token_type != NEWLINE:
                file_tokens.write(f'{token.value}\t\t\t\t{token.token_type}\n')
        print("comments:", self.lexer.comments)

        return self.lexer.errors, self.lexer.comments

    def parse(self):
        lexical_errors, comments = self.tokenize()
        print('------------------------------------------------------------------------')
        file_lex_errors = open("lexical_errors.txt", "w")

        if len(lexical_errors) > 0:
            self.output_errors(file_lex_errors, lexical_errors)
            print("Check lexical_errors.txt for lexical errors")
            return
        else:
            file_lex_errors.write('No lexical errors')

        syntactic_errors, hardware_specifications = self.parser.parse_verilog_code()
        file_syn_errors = open("syntactic_errors.txt", "w")

        if len(syntactic_errors) > 0:
            self.output_errors(file_syn_errors, syntactic_errors)
            print("Check syntactic_errors.txt for syntactic errors")
        else:
            file_syn_errors.write('No syntactic errors')
            file_hware_specifications = open(
                "hardware_specifications.txt", "w")
            file_hware_specifications.write(
                'Identifier\t\tType\t\tDirection\n')
            all_identifiers = set(hardware_specifications.type_dict.keys(
            ) | hardware_specifications.direction_dict.keys())
            for identiier in all_identifiers:
                if hardware_specifications.type_dict.get(identiier)==None:
                    hardware_specifications.type_dict[identiier] = 'null'
                if hardware_specifications.direction_dict.get(identiier)==None:
                    hardware_specifications.direction_dict[identiier] = 'null'
                file_hware_specifications.write(
                    f"{identiier}\t\t\t\t{hardware_specifications.type_dict[identiier]}\t\t\t{hardware_specifications.direction_dict[identiier]}\n")
            print("Hardware specifications listed in hardware_specifications.txt")

    def output_errors(self, output_file, errors):
        output_file.write('Line Num\t\tError\n')
        for error in errors:
            output_file.write(str(error['line_num']))
            output_file.write('\t\t\t\t')
            output_file.write(error['error'])
            output_file.write('\n')


def main():
    code_file = "test_codes/test_3.vlg"
    f = open(code_file, "r")
    lex_obj = VerilogParser(f.read())
    lex_obj.parse()


if __name__ == "__main__":
    main()
