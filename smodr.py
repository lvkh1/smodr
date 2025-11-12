#!/usr/bin/env python3
"""
smodr - A self-modifying meta-language for full recursive expression

This interpreter implements a language that can:
1. Modify its own code during execution
2. Express computations recursively
3. Use the STOP..WORDS vocabulary for control flow
"""

import sys
import re
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass


@dataclass
class Token:
    """Represents a token in the smodr language"""
    type: str
    value: Any
    line: int = 0
    column: int = 0


class SmodrLexer:
    """Lexer for the smodr language"""
    
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        
    def tokenize(self) -> List[Token]:
        """Convert source code into tokens"""
        while self.position < len(self.source):
            self._skip_whitespace()
            if self.position >= len(self.source):
                break
                
            # Skip comments
            if self._peek() == '#':
                self._skip_comment()
                continue
            
            # Keywords from STOP..WORDS
            if self._match_keyword():
                continue
                
            # Numbers
            char = self._peek()
            if char and char != '\0' and char.isdigit():
                self._read_number()
                continue
                
            # Identifiers
            if char and char != '\0' and (char.isalpha() or char == '_'):
                self._read_identifier()
                continue
                
            # Strings
            if self._peek() in ('"', "'"):
                self._read_string()
                continue
                
            # Operators and punctuation
            if self._read_operator():
                continue
                
            # Unknown character
            raise SyntaxError(f"Unexpected character '{self._peek()}' at line {self.line}, column {self.column}")
        
        self.tokens.append(Token('EOF', None, self.line, self.column))
        return self.tokens
    
    def _peek(self, offset=0) -> str:
        """Peek at character without consuming it"""
        pos = self.position + offset
        return self.source[pos] if pos < len(self.source) else '\0'
    
    def _advance(self) -> str:
        """Consume and return current character"""
        if self.position >= len(self.source):
            return '\0'
        char = self.source[self.position]
        self.position += 1
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char
    
    def _skip_whitespace(self):
        """Skip whitespace characters"""
        while self._peek() in ' \t\n\r':
            self._advance()
    
    def _skip_comment(self):
        """Skip comment line"""
        while self._peek() and self._peek() != '\n':
            self._advance()
    
    def _match_keyword(self) -> bool:
        """Try to match a keyword"""
        keywords = [
            'STOP', 'WORDS', 'WAIT', 'WATCH', 'LISTEN', 'PAUSE',
            'CONTEMPLATE', 'EAT', 'DRINK', 'SLEEP', 'REST', 'OBEY',
            # Additional language keywords
            'IF', 'THEN', 'ELSE', 'WHILE', 'DO', 'END',
            'DEFINE', 'CALL', 'RETURN', 'MODIFY', 'RECURSE'
        ]
        
        for keyword in keywords:
            if self.source[self.position:].upper().startswith(keyword.upper()):
                # Check it's not part of a longer identifier
                end_pos = self.position + len(keyword)
                if end_pos >= len(self.source) or not self.source[end_pos].isalnum():
                    self.tokens.append(Token('KEYWORD', keyword.upper(), self.line, self.column))
                    for _ in range(len(keyword)):
                        self._advance()
                    return True
        return False
    
    def _read_number(self):
        """Read a number token"""
        start_col = self.column
        num_str = ''
        while self._peek().isdigit() or self._peek() == '.':
            num_str += self._advance()
        
        value = float(num_str) if '.' in num_str else int(num_str)
        self.tokens.append(Token('NUMBER', value, self.line, start_col))
    
    def _read_identifier(self):
        """Read an identifier token"""
        start_col = self.column
        ident = ''
        while self._peek().isalnum() or self._peek() == '_':
            ident += self._advance()
        self.tokens.append(Token('IDENTIFIER', ident, self.line, start_col))
    
    def _read_string(self):
        """Read a string token"""
        start_col = self.column
        quote = self._advance()  # Opening quote
        string = ''
        
        while self._peek() and self._peek() != quote:
            if self._peek() == '\\':
                self._advance()
                # Handle escape sequences
                escape_char = self._advance()
                escape_map = {'n': '\n', 't': '\t', 'r': '\r', '\\': '\\', quote: quote}
                string += escape_map.get(escape_char, escape_char)
            else:
                string += self._advance()
        
        if not self._peek():
            raise SyntaxError(f"Unterminated string at line {self.line}")
        
        self._advance()  # Closing quote
        self.tokens.append(Token('STRING', string, self.line, start_col))
    
    def _read_operator(self) -> bool:
        """Read operator or punctuation"""
        char = self._peek()
        operators = {
            '+': 'PLUS', '-': 'MINUS', '*': 'MULTIPLY', '/': 'DIVIDE',
            '=': 'ASSIGN', '(': 'LPAREN', ')': 'RPAREN',
            '{': 'LBRACE', '}': 'RBRACE', '[': 'LSQUARE', ']': 'RSQUARE',
            ',': 'COMMA', ';': 'SEMICOLON', ':': 'COLON',
            '?': 'QUESTION', '!': 'EXCLAIM', '.': 'DOT',
            '<': 'LT', '>': 'GT'
        }
        
        # Two-character operators
        two_char = self._peek() + self._peek(1)
        if two_char in ['==', '!=', '<=', '>=', '..']:
            self.tokens.append(Token(two_char, two_char, self.line, self.column))
            self._advance()
            self._advance()
            return True
        
        if char in operators:
            self.tokens.append(Token(operators[char], char, self.line, self.column))
            self._advance()
            return True
        
        return False


class SmodrEnvironment:
    """Execution environment for smodr programs"""
    
    def __init__(self, parent: Optional['SmodrEnvironment'] = None):
        self.parent = parent
        self.variables: Dict[str, Any] = {}
        self.functions: Dict[str, Callable] = {}
        self.source_code: str = ""  # For self-modification
        
    def define(self, name: str, value: Any):
        """Define a variable in this environment"""
        self.variables[name] = value
    
    def get(self, name: str) -> Any:
        """Get a variable from this environment or parent"""
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.get(name)
        raise NameError(f"Undefined variable: {name}")
    
    def set(self, name: str, value: Any):
        """Set a variable in this environment or parent"""
        if name in self.variables:
            self.variables[name] = value
        elif self.parent and self.parent.has(name):
            self.parent.set(name, value)
        else:
            self.variables[name] = value
    
    def has(self, name: str) -> bool:
        """Check if variable exists"""
        return name in self.variables or (self.parent and self.parent.has(name))
    
    def get_function(self, name: str) -> Optional[Callable]:
        """Get a function from this environment or parent"""
        if name in self.functions:
            return self.functions[name]
        if self.parent:
            return self.parent.get_function(name)
        return None


class SmodrInterpreter:
    """Interpreter for the smodr language"""
    
    def __init__(self):
        self.global_env = SmodrEnvironment()
        self._setup_builtins()
    
    def _setup_builtins(self):
        """Setup built-in functions"""
        self.global_env.functions['print'] = lambda *args: print(*args)
        self.global_env.functions['input'] = lambda prompt="": input(prompt)
        self.global_env.functions['str'] = str
        self.global_env.functions['int'] = int
        self.global_env.functions['float'] = float
    
    def interpret(self, source: str) -> Any:
        """Interpret smodr source code"""
        self.global_env.source_code = source
        
        # Tokenize
        lexer = SmodrLexer(source)
        tokens = lexer.tokenize()
        
        # Parse and execute
        parser = SmodrParser(tokens)
        ast = parser.parse()
        
        # Execute
        return self._execute(ast, self.global_env)
    
    def _execute(self, node: Any, env: SmodrEnvironment) -> Any:
        """Execute an AST node"""
        if node is None:
            return None
        
        node_type = node.get('type')
        
        if node_type == 'PROGRAM':
            result = None
            for statement in node.get('statements', []):
                result = self._execute(statement, env)
            return result
        
        elif node_type == 'NUMBER':
            return node['value']
        
        elif node_type == 'STRING':
            return node['value']
        
        elif node_type == 'IDENTIFIER':
            return env.get(node['value'])
        
        elif node_type == 'ASSIGN':
            value = self._execute(node['value'], env)
            env.define(node['name'], value)
            return value
        
        elif node_type == 'BINARY_OP':
            left = self._execute(node['left'], env)
            right = self._execute(node['right'], env)
            op = node['operator']
            
            ops = {
                '+': lambda a, b: a + b,
                '-': lambda a, b: a - b,
                '*': lambda a, b: a * b,
                '/': lambda a, b: a / b,
                '==': lambda a, b: a == b,
                '!=': lambda a, b: a != b,
                '<': lambda a, b: a < b,
                '>': lambda a, b: a > b,
                '<=': lambda a, b: a <= b,
                '>=': lambda a, b: a >= b,
            }
            
            return ops.get(op, lambda a, b: None)(left, right)
        
        elif node_type == 'FUNCTION_CALL':
            func_name = node['name']
            args = [self._execute(arg, env) for arg in node.get('arguments', [])]
            
            func = env.get_function(func_name)
            if func:
                return func(*args)
            else:
                raise NameError(f"Undefined function: {func_name}")
        
        elif node_type == 'IF':
            condition = self._execute(node['condition'], env)
            if condition:
                return self._execute(node['then_branch'], env)
            elif 'else_branch' in node:
                return self._execute(node['else_branch'], env)
        
        elif node_type == 'WHILE':
            result = None
            while self._execute(node['condition'], env):
                result = self._execute(node['body'], env)
            return result
        
        elif node_type == 'DEFINE':
            func_name = node['name']
            params = node['parameters']
            body = node['body']
            
            def user_function(*args):
                local_env = SmodrEnvironment(env)
                for param, arg in zip(params, args):
                    local_env.define(param, arg)
                result = self._execute(body, local_env)
                # Check if the result is a return value
                if isinstance(result, dict) and result.get('_return'):
                    return result['value']
                return result
            
            env.functions[func_name] = user_function
            return None
        
        elif node_type == 'RETURN':
            value = self._execute(node['value'], env)
            return {'_return': True, 'value': value}
        
        elif node_type == 'RECURSE':
            # Special handling for recursive calls
            func_name = node.get('function', '__current__')
            args = [self._execute(arg, env) for arg in node.get('arguments', [])]
            
            func = env.get_function(func_name)
            if func:
                return func(*args)
        
        elif node_type == 'MODIFY':
            # Self-modification capability
            target = node['target']
            new_code = self._execute(node['code'], env)
            
            if target == 'source':
                env.source_code = new_code
                # Re-interpret the modified source
                return self.interpret(new_code)
        
        elif node_type == 'BLOCK':
            result = None
            for statement in node.get('statements', []):
                result = self._execute(statement, env)
                # Propagate return values
                if isinstance(result, dict) and result.get('_return'):
                    return result
            return result
        
        return None


class SmodrParser:
    """Parser for the smodr language"""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.position = 0
    
    def parse(self) -> Dict:
        """Parse tokens into AST"""
        statements = []
        
        while not self._is_at_end():
            if self._peek().type == 'EOF':
                break
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
        
        return {'type': 'PROGRAM', 'statements': statements}
    
    def _parse_statement(self) -> Optional[Dict]:
        """Parse a single statement"""
        token = self._peek()
        
        if token.type == 'KEYWORD':
            keyword = token.value
            
            if keyword == 'DEFINE':
                return self._parse_define()
            elif keyword == 'IF':
                return self._parse_if()
            elif keyword == 'WHILE':
                return self._parse_while()
            elif keyword == 'MODIFY':
                return self._parse_modify()
            elif keyword == 'RECURSE':
                return self._parse_recurse()
            elif keyword == 'RETURN':
                self._advance()
                return {'type': 'RETURN', 'value': self._parse_expression()}
            elif keyword in ['STOP', 'PAUSE', 'WAIT']:
                # Control flow keywords - for now, treat as no-op
                self._advance()
                return None
        
        # Expression statement or assignment
        return self._parse_expression_statement()
    
    def _parse_expression_statement(self) -> Optional[Dict]:
        """Parse expression or assignment"""
        expr = self._parse_expression()
        
        # Check for assignment
        if self._peek().type == 'ASSIGN':
            self._advance()
            if expr.get('type') == 'IDENTIFIER':
                value = self._parse_expression()
                return {'type': 'ASSIGN', 'name': expr['value'], 'value': value}
        
        return expr
    
    def _parse_expression(self) -> Dict:
        """Parse an expression"""
        return self._parse_comparison()
    
    def _parse_comparison(self) -> Dict:
        """Parse comparison expression"""
        left = self._parse_term()
        
        while self._peek().type in ['==', '!=', 'LT', 'GT', '<=', '>=']:
            token = self._advance()
            op = token.value
            right = self._parse_term()
            left = {'type': 'BINARY_OP', 'operator': op, 'left': left, 'right': right}
        
        return left
    
    def _parse_term(self) -> Dict:
        """Parse term (addition/subtraction)"""
        left = self._parse_factor()
        
        while self._peek().type in ['PLUS', 'MINUS']:
            op = self._advance().value
            right = self._parse_factor()
            left = {'type': 'BINARY_OP', 'operator': op, 'left': left, 'right': right}
        
        return left
    
    def _parse_factor(self) -> Dict:
        """Parse factor (multiplication/division)"""
        left = self._parse_primary()
        
        while self._peek().type in ['MULTIPLY', 'DIVIDE']:
            op = self._advance().value
            right = self._parse_primary()
            left = {'type': 'BINARY_OP', 'operator': op, 'left': left, 'right': right}
        
        return left
    
    def _parse_primary(self) -> Dict:
        """Parse primary expression"""
        token = self._peek()
        
        if token.type == 'NUMBER':
            self._advance()
            return {'type': 'NUMBER', 'value': token.value}
        
        if token.type == 'STRING':
            self._advance()
            return {'type': 'STRING', 'value': token.value}
        
        if token.type == 'IDENTIFIER':
            self._advance()
            # Check for function call
            if self._peek().type == 'LPAREN':
                return self._parse_function_call(token.value)
            return {'type': 'IDENTIFIER', 'value': token.value}
        
        if token.type == 'LPAREN':
            self._advance()
            expr = self._parse_expression()
            if self._peek().type != 'RPAREN':
                raise SyntaxError("Expected ')'")
            self._advance()
            return expr
        
        raise SyntaxError(f"Unexpected token: {token.type}")
    
    def _parse_function_call(self, name: str) -> Dict:
        """Parse function call"""
        self._advance()  # consume LPAREN
        
        arguments = []
        if self._peek().type != 'RPAREN':
            arguments.append(self._parse_expression())
            
            while self._peek().type == 'COMMA':
                self._advance()
                arguments.append(self._parse_expression())
        
        if self._peek().type != 'RPAREN':
            raise SyntaxError("Expected ')'")
        self._advance()
        
        return {'type': 'FUNCTION_CALL', 'name': name, 'arguments': arguments}
    
    def _parse_define(self) -> Dict:
        """Parse function definition"""
        self._advance()  # consume DEFINE
        
        if self._peek().type != 'IDENTIFIER':
            raise SyntaxError("Expected function name")
        
        func_name = self._advance().value
        
        # Parse parameters
        parameters = []
        if self._peek().type == 'LPAREN':
            self._advance()
            if self._peek().type != 'RPAREN':
                if self._peek().type != 'IDENTIFIER':
                    raise SyntaxError("Expected parameter name")
                parameters.append(self._advance().value)
                
                while self._peek().type == 'COMMA':
                    self._advance()
                    if self._peek().type != 'IDENTIFIER':
                        raise SyntaxError("Expected parameter name")
                    parameters.append(self._advance().value)
            
            if self._peek().type != 'RPAREN':
                raise SyntaxError("Expected ')'")
            self._advance()
        
        # Parse body
        body = self._parse_block()
        
        return {'type': 'DEFINE', 'name': func_name, 'parameters': parameters, 'body': body}
    
    def _parse_if(self) -> Dict:
        """Parse if statement"""
        self._advance()  # consume IF
        
        condition = self._parse_expression()
        
        # Optional THEN keyword
        if self._peek().type == 'KEYWORD' and self._peek().value == 'THEN':
            self._advance()
        
        then_branch = self._parse_block()
        
        else_branch = None
        if self._peek().type == 'KEYWORD' and self._peek().value == 'ELSE':
            self._advance()
            else_branch = self._parse_block()
        
        return {'type': 'IF', 'condition': condition, 'then_branch': then_branch, 'else_branch': else_branch}
    
    def _parse_while(self) -> Dict:
        """Parse while loop"""
        self._advance()  # consume WHILE
        
        condition = self._parse_expression()
        
        # Optional DO keyword
        if self._peek().type == 'KEYWORD' and self._peek().value == 'DO':
            self._advance()
        
        body = self._parse_block()
        
        return {'type': 'WHILE', 'condition': condition, 'body': body}
    
    def _parse_modify(self) -> Dict:
        """Parse self-modification statement"""
        self._advance()  # consume MODIFY
        
        if self._peek().type != 'IDENTIFIER':
            raise SyntaxError("Expected target for modification")
        
        target = self._advance().value
        code = self._parse_expression()
        
        return {'type': 'MODIFY', 'target': target, 'code': code}
    
    def _parse_recurse(self) -> Dict:
        """Parse recursive call"""
        self._advance()  # consume RECURSE
        
        arguments = []
        if self._peek().type == 'LPAREN':
            self._advance()
            if self._peek().type != 'RPAREN':
                arguments.append(self._parse_expression())
                
                while self._peek().type == 'COMMA':
                    self._advance()
                    arguments.append(self._parse_expression())
            
            if self._peek().type != 'RPAREN':
                raise SyntaxError("Expected ')'")
            self._advance()
        
        return {'type': 'RECURSE', 'arguments': arguments}
    
    def _parse_block(self) -> Dict:
        """Parse a block of statements"""
        statements = []
        
        # Check for explicit block with braces
        if self._peek().type == 'LBRACE':
            self._advance()
            while self._peek().type != 'RBRACE' and not self._is_at_end():
                stmt = self._parse_statement()
                if stmt:
                    statements.append(stmt)
            
            if self._peek().type != 'RBRACE':
                raise SyntaxError("Expected '}'")
            self._advance()
        else:
            # Multiple statements until END keyword or EOF
            while not self._is_at_end():
                # Stop if we encounter END
                if self._peek().type == 'KEYWORD' and self._peek().value == 'END':
                    break
                
                # Stop if we encounter another control flow keyword that starts a new block
                if self._peek().type == 'KEYWORD' and self._peek().value in ['ELSE', 'ELIF']:
                    break
                
                stmt = self._parse_statement()
                if stmt:
                    statements.append(stmt)
        
        # Check for END keyword
        if self._peek().type == 'KEYWORD' and self._peek().value == 'END':
            self._advance()
        
        return {'type': 'BLOCK', 'statements': statements}
    
    def _peek(self) -> Token:
        """Peek at current token"""
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return Token('EOF', None)
    
    def _advance(self) -> Token:
        """Consume and return current token"""
        token = self._peek()
        if not self._is_at_end():
            self.position += 1
        return token
    
    def _is_at_end(self) -> bool:
        """Check if at end of tokens"""
        return self.position >= len(self.tokens) or self._peek().type == 'EOF'


def main():
    """Main entry point for the smodr interpreter"""
    if len(sys.argv) > 1:
        # Execute file
        filename = sys.argv[1]
        try:
            with open(filename, 'r') as f:
                source = f.read()
            
            interpreter = SmodrInterpreter()
            result = interpreter.interpret(source)
            
            if result is not None:
                print(result)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # REPL mode
        print("smodr v0.1.0 - Self-modifying meta-language")
        print("Type 'exit' to quit")
        print()
        
        interpreter = SmodrInterpreter()
        
        while True:
            try:
                source = input("smodr> ")
                if source.strip().lower() == 'exit':
                    break
                
                if source.strip():
                    result = interpreter.interpret(source)
                    if result is not None:
                        print(result)
            except KeyboardInterrupt:
                print("\nKeyboardInterrupt")
                break
            except EOFError:
                break
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)


if __name__ == '__main__':
    main()
