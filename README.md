# Parser for Verilog in Python

- The folder contains various files - 
    1) token.py - Defines various verilog tokens and module item types.
    2) constants.py - Defines constants used in verilog code.
    3) helper_functions.py - Some helper functions used to check token types.
    4) token_class.py - Defines a class to represent a token.
    5) hardware_specification.py - Defines a class which stores all the hardware specifications along with their type (wire/register) and port-type (input/output/inout)
    6) lexical_analyser.py - Defines a VerilogLexer class which tokenizes the verilog code.
    7) syntax_analyser.py - Defines a VerilogSyntaxAnalyser class which uses the tokens provided by the lexer and checks for syntax errors in the code.
    8) verilog_parser.py - Defines a VerilogParser which uses the VerilogLexer and VerilogSyntaxAnalyser to output lexical and syntactic errors in code file.

- Following are the instructions for using the code - 
    1) Assign the path for the file to be parsed to 'code_file' variable in main function of verilog_parser.py file. <br/>
        <b>OR</b>
        Copy the code that needs to be parsed to demofile.vlg file.
    2) Using a python interpreter run the verilog_parser (as the main function of parser calls the parse method).
    3) The output after running will be - <br/>
        a) Tokens : symbol_table.txt generated in folder listing all tokens along with their token type. <br/>
        b) All the comments in Verilog Code : In the console. <br/>
        c) Lexical errors : lexical_errors.txt generated in folder listing all lexical errors with line numbers.<br/>
        d) Syntactic errors : 
            i) Generated only when no lexical errors are present.
            ii) If no lexical errors present - syntactic_errors.txt generated in folder listing all syntactic errors with line numbers.
        e) Functions in modules : List of all functions present in a module are shown in the console for each module in the code file.
        f) Hardware specifications : List of all hardware specifications used in a file are generated in the hardware_specifications.txt file.

- Sample test codes that can be used for testing are added in the 'test_codes' folder.








