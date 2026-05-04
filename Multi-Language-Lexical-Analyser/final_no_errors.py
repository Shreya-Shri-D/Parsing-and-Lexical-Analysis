import sys
from pathlib import Path

from tabulate import tabulate

_ROOT = Path(__file__).resolve().parent

# Token class for C, Java, and C++
class Token:
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value

# C Lexer
class CLexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.keywords = self.get_keywords()  # C keywords
        self.operators = self.get_operators()  # C operators
        self.standard_functions = self.get_standard_functions()  # C Standard Functions
        self.current_state = 'start'  # Initial state
        self.current_token = ''  # Current token being constructed

    def get_keywords(self):
        return set([
            'auto', 'break', 'case', 'char', 'const', 'continue', 'default',
            'do', 'double', 'else', 'enum', 'extern', 'float', 'for', 'goto',
            'if', 'inline', 'int', 'long', 'register', 'restrict', 'return',
            'short', 'signed', 'sizeof', 'static', 'struct', 'switch',
            'typedef', 'union', 'unsigned', 'void', 'volatile', 'while'
        ])

    def get_operators(self):
        return set([
            '==', '!=', '>=', '<=', '++', '--', '+=', '-=', '*=', '/=', '%=',
            '&&', '||', '>', '<', '+', '-', '*', '/', '%', '=', '!', '&',
            '|', '^', '<<', '>>', '~'
        ])

    def get_standard_functions(self):
        return set([
            'printf', 'scanf', 'malloc', 'free', 'exit', 'fopen', 'fclose',
            'fgets', 'fputs', 'fprintf', 'fscanf', 'strcpy', 'strcat',
            'strlen', 'strcmp', 'atoi', 'atof', 'abs', 'pow', 'sqrt'
        ])

    def add_token(self, token_type):
        if self.current_token:  # Only add if there's a current token
            # Check if the token is a standard function
            if token_type == 'Identifier' and self.current_token in self.standard_functions:
                self.tokens.append(Token('Standard Function', self.current_token))
            else:
                self.tokens.append(Token(token_type, self.current_token))
        self.current_token = ''  # Reset current token

    def transition(self, char):
        if self.current_state == 'start':
            if char == '#':
                self.current_state = 'preprocessor'
                self.current_token = char
            elif char.isalpha() or char == '_':
                self.current_state = 'identifier'
                self.current_token += char
            elif char.isdigit():
                self.current_state = 'number'
                self.current_token += char
            elif char in ('"', "'"):
                self.current_state = 'string'
                self.current_token += char
            elif char in '(){};,.':
                self.tokens.append(Token('Symbol', char))  # Add single character symbols
            elif char in self.operators:
                self.current_token = char  # Start building an operator
                self.current_state = 'operator'
            elif char.isspace():
                pass  # Ignore whitespace
            else:
                self.current_token += char  # Any other character

        elif self.current_state == 'preprocessor':
            if char.isspace():
                if self.current_token == '#include':
                    self.add_token('Preprocessor')
                    self.current_state = 'header'
            else:
                self.current_token += char  # Continue collecting the preprocessor keyword

        elif self.current_state == 'header':
            if char == '<':
                self.current_token = char  # Start of a system header
            elif char == '>':
                self.current_token += char  # End of the header
                self.add_token('Header')  # Add token as Header
                self.current_state = 'start'
            else:
                self.current_token += char  # Collecting header name

        elif self.current_state == 'identifier':
            if char.isalnum() or char == '_':
                self.current_token += char
            else:
                if self.current_token in self.keywords:
                    self.add_token('Keyword')
                else:
                    self.add_token('Identifier')
                self.current_state = 'start'
                self.transition(char)  # Process the next character

        elif self.current_state == 'number':
            if char.isdigit() or char == '.':
                self.current_token += char
            else:
                self.add_token('Number')
                self.current_state = 'start'
                self.transition(char)  # Process the next character

        elif self.current_state == 'string':
            self.current_token += char
            if char == self.current_token[0]:  # End of string
                self.add_token('String')
                self.current_state = 'start'

        elif self.current_state == 'operator':
            # Check if the operator can continue (like `==` or `+=`)
            if self.current_token + char in self.operators:
                self.current_token += char
            else:
                self.add_token('Operator')  # Finalize the operator
                self.current_state = 'start'
                self.transition(char)  # Process the next character

    def tokenize(self):
        for char in self.code:
            self.transition(char)
        # Add any remaining token after the loop
        if self.current_token:
            if self.current_state == 'identifier':
                if self.current_token in self.keywords:
                    self.add_token('Keyword')
                else:
                    self.add_token('Identifier')
            elif self.current_state == 'number':
                self.add_token('Number')
            elif self.current_state == 'string':
                self.add_token('String')
            elif self.current_state == 'operator':
                self.add_token('Operator')

        return self.tokens

# Java Lexer
class JavaLexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.keywords = self.get_keywords()  # Java keywords
        self.operators = self.get_operators()  # Java operators
        self.standard_functions = self.get_standard_functions()  # Java Standard Functions
        self.class_names = self.get_class_names()  # Java Class Names
        self.current_state = 'start'  # Initial state
        self.current_token = ''  # Current token being constructed

    def get_keywords(self):
        return set([
            'abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch',
            'char', 'class', 'const', 'continue', 'default', 'do', 'double',
            'else', 'enum', 'extends', 'final', 'finally', 'float', 'for',
            'if', 'implements', 'import', 'instanceof', 'int', 'interface',
            'long', 'native', 'new', 'package', 'private', 'protected',
            'public', 'return', 'short', 'static', 'strictfp', 'super',
            'switch', 'synchronized', 'this', 'throw', 'throws', 'transient',
            'try', 'void', 'volatile', 'while'
        ])

    def get_operators(self):
        return set([
            '==', '!=', '>=', '<=', '++', '--', '+=', '-=', '*=', '/=', '%=',
            '&&', '||', '>', '<', '+', '-', '*', '/', '%', '=', '!', '&',
            '|', '^', '<<', '>>', '~'
        ])

    def get_standard_functions(self):
        return set([
            'System.out.println', 'System.out.print', 'Math.abs', 'Math.max', 
            'Math.min', 'Math.sqrt', 'Integer.parseInt', 'Double.parseDouble'
        ])

    def get_class_names(self):
        return set(['String', 'Integer', 'Double', 'Math'])

    def add_token(self, token_type):
        if self.current_token:  # Only add if there's a current token
            # Check if the token is a class name
            if self.current_token in self.class_names:
                self.tokens.append(Token('Class Name', self.current_token))
            # Check if the token is a standard function
            elif token_type == 'Identifier' and self.current_token in self.standard_functions:
                self.tokens.append(Token('Standard Function', self.current_token))
            else:
                self.tokens.append(Token(token_type, self.current_token))
        self.current_token = ''  # Reset current token

    def transition(self, char):
        if self.current_state == 'start':
            if char.isalpha() or char == '_':
                self.current_state = 'identifier'
                self.current_token += char
            elif char.isdigit():
                self.current_state = 'number'
                self.current_token += char
            elif char in ('"', "'"):
                self.current_state = 'string'
                self.current_token += char
            elif char in '(){};,.':
                self.tokens.append(Token('Symbol', char))  # Add single character symbols
            elif char in self.operators:
                self.current_token += char  # Start building an operator
                self.current_state = 'operator'
            elif char.isspace():
                pass  # Ignore whitespace
            else:
                self.current_token += char  # Any other character

        elif self.current_state == 'identifier':
            if char == '.':
                self.current_token += char
            elif char.isalnum() or char == '_':
                self.current_token += char
            else:
                if self.current_token in self.keywords:
                    self.add_token('Keyword')
                elif 'System.out' in self.current_token:  # Check for System.out calls
                    self.add_token('Standard Function')  # Handle System.out specifically
                else:
                    self.add_token('Identifier')
                self.current_state = 'start'
                self.transition(char)  # Process the next character

        elif self.current_state == 'number':
            if char.isdigit() or char == '.':
                self.current_token += char
            else:
                self.add_token('Number')
                self.current_state = 'start'
                self.transition(char)  # Process the next character

        elif self.current_state == 'string':
            self.current_token += char
            if char == self.current_token[0]:  # End of string
                self.add_token('String')
                self.current_state = 'start'

        elif self.current_state == 'operator':
            # Check if the operator can continue (like `==` or `+=`)
            if self.current_token + char in self.operators:
                self.current_token += char
            else:
                self.add_token('Operator')  # Finalize the operator
                self.current_state = 'start'
                self.transition(char)  # Process the next character

    def tokenize(self):
        for char in self.code:
            self.transition(char)
        # Add any remaining token after the loop
        if self.current_token:
            if self.current_state == 'identifier':
                if self.current_token in self.keywords:
                    self.add_token('Keyword')
                else:
                    self.add_token('Identifier')
            elif self.current_state == 'number':
                self.add_token('Number')
            elif self.current_state == 'string':
                self.add_token('String')
            elif self.current_state == 'operator':
                self.add_token('Operator')

        return self.tokens

# C++ Lexer
class CppLexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.keywords = self.get_keywords()  # C++ keywords
        self.operators = self.get_operators()  # C++ operators
        self.standard_functions = self.get_standard_functions()  # C++ Standard Functions
        self.class_names = self.get_class_names()  # C++ Class Names
        self.current_state = 'start'  # Initial state
        self.current_token = ''  # Current token being constructed

    def get_keywords(self):
        return set([
            'alignas', 'alignof', 'and', 'and_eq', 'asm', 'auto', 'bitand', 
            'bitor', 'bool', 'break', 'case', 'catch', 'char', 'char8_t', 
            'char16_t', 'char32_t', 'class', 'compl', 'concept', 'const', 
            'constexpr', 'const_cast', 'continue', 'co_await', 'co_return', 
            'decltype', 'default', 'delete', 'do', 'double', 'dynamic_cast', 
            'else', 'enum', 'explicit', 'export', 'extern', 'false', 'float', 
            'for', 'friend', 'goto', 'if', 'inline', 'int', 'long', 'mutable', 
            'namespace', 'new', 'noexcept', 'not', 'not_eq', 'nullptr', 
            'operator', 'or', 'or_eq', 'private', 'protected', 'public', 
            'reflexpr', 'register', 'reinterpret_cast', 'requires', 'return', 
            'short', 'signed', 'sizeof', 'static', 'static_assert', 'static_cast', 
            'struct', 'switch', 'template', 'this', 'thread_local', 'throw', 
            'true', 'try', 'typedef', 'typeid', 'typename', 'union', 
            'unsigned', 'using', 'virtual', 'void', 'volatile', 'wchar_t', 
            'while', 'xor', 'xor_eq'
        ])

    def get_operators(self):
        return set([
            '==', '!=', '>=', '<=', '++', '--', '+=', '-=', '*=', '/=', '%=',
            '&&', '||', '>', '<', '+', '-', '*', '/', '%', '=', '!', '&',
            '|', '^', '<<', '>>', '~', '->', '::'
        ])

    def get_standard_functions(self):
        return set([
            'std::cout', 'std::cin', 'std::endl', 'std::string', 'std::vector', 
            'std::map', 'std::set', 'std::abs', 'std::pow', 'std::sqrt'
        ])

    def get_class_names(self):
        return set(['std::string', 'std::vector', 'std::map', 'std::set'])

    def add_token(self, token_type):
        if self.current_token:  # Only add if there's a current token
            # Check if the token is a class name
            if self.current_token in self.class_names:
                self.tokens.append(Token('Class Name', self.current_token))
            # Check if the token is a standard function
            elif token_type == 'Identifier' and self.current_token in self.standard_functions:
                self.tokens.append(Token('Standard Function', self.current_token))
            else:
                self.tokens.append(Token(token_type, self.current_token))
        self.current_token = ''  # Reset current token

    def transition(self, char):
        if self.current_state == 'start':
            if char == '#':
                self.current_state = 'preprocessor'
                self.current_token += char
            elif char.isalpha() or char == '_':
                self.current_state = 'identifier'
                self.current_token += char
            elif char.isdigit():
                self.current_state = 'number'
                self.current_token += char
            elif char in ('"', "'"):
                self.current_state = 'string'
                self.current_token += char
            elif char in '(){};,.':
                self.tokens.append(Token('Symbol', char))  # Add single character symbols
            elif char in self.operators:
                self.current_token += char  # Start building an operator
                self.current_state = 'operator'
            elif char.isspace():
                pass  # Ignore whitespace
            else:
                self.current_token += char  # Any other character
    
        elif self.current_state == 'preprocessor':
            if char.isspace():
                if self.current_token == '#include':
                    self.add_token('Preprocessor')  # Add as Preprocessor
                    self.current_state = 'header'
            else:
                self.current_token += char  # Continue collecting the preprocessor keyword
    
        elif self.current_state == 'header':
            if char == '<':
                self.current_token = char  # Start of a system header
            elif char == '>':
                self.current_token += char  # End of the header
                self.add_token('Header')  # Add token as Header
                self.current_state = 'start'
            else:
                self.current_token += char  # Collecting header name
    
        elif self.current_state == 'identifier':
            if char.isalnum() or char == '_' or char == ':':  # Support '::' in identifiers
                self.current_token += char
            else:
                if self.current_token.startswith('std::'):  # Handle std:: namespace
                    if self.current_token in self.standard_functions:
                        self.add_token('Standard Function')
                    else:
                        self.add_token('Identifier')  # Fallback if not a standard function
                elif self.current_token in self.class_names:
                    self.add_token('Class Name')
                elif self.current_token in self.keywords:
                    self.add_token('Keyword')
                else:
                    self.add_token('Identifier')
                self.current_state = 'start'
                self.transition(char)  # Process the next character
    
        elif self.current_state == 'number':
            if char.isdigit() or char == '.':
                self.current_token += char
            else:
                self.add_token('Number')
                self.current_state = 'start'
                self.transition(char)  # Process the next character
    
        elif self.current_state == 'string':
            self.current_token += char
            if char == self.current_token[0]:  # End of string
                self.add_token('String')
                self.current_state = 'start'
    
        elif self.current_state == 'operator':
            # Check if the operator can continue (like `==` or `+=`)
            if self.current_token + char in self.operators:
                self.current_token += char
            else:
                self.add_token('Operator')  # Finalize the operator
                self.current_state = 'start'
                self.transition(char)  # Process the next character


    def tokenize(self):
        for char in self.code:
            self.transition(char)
        # Add any remaining token after the loop
        if self.current_token:
            if self.current_state == 'identifier':
                if self.current_token in self.keywords:
                    self.add_token('Keyword')
                else:
                    self.add_token('Identifier')
            elif self.current_state == 'number':
                self.add_token('Number')
            elif self.current_state == 'string':
                self.add_token('String')
            elif self.current_state == 'operator':
                self.add_token('Operator')

        return self.tokens


def generate_token_table(tokens):
    table = []
    for token in tokens:
        table.append([token.token_type, token.value])
    return table

# Default: pal.c in this folder; override: python final_no_errors.py pal.java
file_path = Path(sys.argv[1]) if len(sys.argv) > 1 else (_ROOT / "pal.c")
if not file_path.is_absolute():
    file_path = _ROOT / file_path

# Read the content of the file
with open(file_path, "r", encoding="utf-8") as file:
    code = file.read()

# Determine the language based on the file extension
suffix = file_path.suffix.lower()
if suffix == ".java":
    lexer = JavaLexer(code)
    tokens = lexer.tokenize()
elif suffix == ".c":
    lexer = CLexer(code)
    tokens = lexer.tokenize()
elif suffix == ".cpp":  # Add C++ lexer handling
    lexer = CppLexer(code)
    tokens = lexer.tokenize()
else:
    raise ValueError("Unsupported file type")

token_table = generate_token_table(tokens)

# Print token table
print(tabulate(token_table, headers=["Token Type", "Value"], tablefmt="grid"))
