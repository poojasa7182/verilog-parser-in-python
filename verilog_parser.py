from lexical_analyser import *
from syntax_analyser import *


class VerilogParser:
    '''
    Class to represent Verilog Parser
    '''

    def __init__(self, code):
        self.lexer = VerilogLexer(code)
        self.parser = VerilogSyntaxAnalyser(code)

    def tokenize(self):
        while True:
            token = self.lexer.get_next_token()
            if token.token_type is EOF:
                break
            if token.token_type != NEWLINE:
                pass
        #         print(token.value, '->', token.token_type)
        # print("comments:", self.lexer.comments)
        # print("lexical errors:", self.lexer.errors)

        return self.lexer.errors, self.lexer.comments

    def parse(self):
        lexical_errors, comments = self.tokenize()
        file_lex_errors = open("lexical_errors.txt", "w")
        if len(lexical_errors) > 0:
            file_lex_errors.write('Line Num')
            file_lex_errors.write('\t\t')
            file_lex_errors.write('Error')
            file_lex_errors.write('\n')
            for lexical_error in lexical_errors:
                file_lex_errors.write(str(lexical_error['line_num']))
                file_lex_errors.write('\t\t\t\t')
                file_lex_errors.write(lexical_error['error'])
                file_lex_errors.write('\n')
            print("Check lexical_errors.txt for lexical errors")
            return
        else:
            file_lex_errors.write('No lexical errors')
        syntactic_errors = self.parser.parse_verilog_code()
        file_syn_errors = open("syntactic_errors.txt", "w")
        if len(syntactic_errors) > 0:
            file_syn_errors.write('Line Num')
            file_syn_errors.write('\t\t')
            file_syn_errors.write('Error')
            file_syn_errors.write('\n')
            for syntactic_error in syntactic_errors:
                file_syn_errors.write(str(syntactic_error['line_num']))
                file_syn_errors.write('\t\t\t\t')
                file_syn_errors.write(syntactic_error['error'])
                file_syn_errors.write('\n')
            print("Check syntactic_errors.txt for syntactic errors")
        else:
            file_syn_errors.write('No syntactic errors')


def main():
    code_file = "demofile.vlg"
    f = open(code_file, "r")
    lex_obj = VerilogParser(f.read())
    lex_obj.parse()


if __name__ == "__main__":
    main()
