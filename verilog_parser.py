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
        file_tokens.write('TOKEN')
        file_tokens.write('\t\t\t')
        file_tokens.write('TOKEN TYPE')
        file_tokens.write('\n')
        file_tokens.write('\n')
        while True:
            token = self.lexer.get_next_token()
            if token.token_type is EOF:
                break
            if token.token_type != NEWLINE:
                file_tokens.write(token.value)
                file_tokens.write('\t\t\t\t')
                file_tokens.write(token.token_type)
                file_tokens.write('\n')
        print("comments:", self.lexer.comments)

        return self.lexer.errors, self.lexer.comments

    def parse(self):
        lexical_errors, comments = self.tokenize()
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
            file_hware_specifications = open("hardware_specifications.txt", "w")
            file_hware_specifications.write('Identifier\t\tType\t\tDirection\n')
            all_identifiers = set(hardware_specifications.type_dict.keys() | hardware_specifications.direction_dict.keys())
            for identiier in all_identifiers:
                file_hware_specifications.write(f"{identiier}\t\t\t\t{hardware_specifications.type_dict[identiier]}\t\t\t{hardware_specifications.direction_dict[identiier]}\n")
            print("Hardware specifications listed in hardware_specifications.txt")

    def output_errors(self, output_file, errors):
        output_file.write('Line Num')
        output_file.write('\t\t')
        output_file.write('Error')
        output_file.write('\n')
        for error in errors:
            output_file.write(str(error['line_num']))
            output_file.write('\t\t\t\t')
            output_file.write(error['error'])
            output_file.write('\n')

    # def output_hardware_specifications(output_file, hardware_specifications):
    #     output_file.write('Identifier\t\tType\t\tDirection')
    #     all_identifiers = hardware_specifications.type_dict.keys() | hardware_specifications.

def main():
    code_file = "demofile.vlg"
    f = open(code_file, "r")
    lex_obj = VerilogParser(f.read())
    lex_obj.parse()


if __name__ == "__main__":
    main()
