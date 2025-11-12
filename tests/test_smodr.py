#!/usr/bin/env python3
"""
Test suite for smodr language interpreter
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from smodr import SmodrInterpreter, SmodrLexer, SmodrParser


def test_arithmetic():
    """Test basic arithmetic operations"""
    interpreter = SmodrInterpreter()
    
    assert interpreter.interpret("5 + 3") == 8
    assert interpreter.interpret("10 - 4") == 6
    assert interpreter.interpret("6 * 7") == 42
    assert interpreter.interpret("20 / 4") == 5
    assert interpreter.interpret("(2 + 3) * 4") == 20
    
    print("✓ Arithmetic tests passed")


def test_variables():
    """Test variable assignment and retrieval"""
    interpreter = SmodrInterpreter()
    
    result = interpreter.interpret("""
x = 10
y = 20
x + y
""")
    assert result == 30
    
    print("✓ Variable tests passed")


def test_comparisons():
    """Test comparison operations"""
    interpreter = SmodrInterpreter()
    
    assert interpreter.interpret("5 < 10") == True
    assert interpreter.interpret("10 > 5") == True
    assert interpreter.interpret("5 == 5") == True
    assert interpreter.interpret("5 != 10") == True
    assert interpreter.interpret("5 <= 5") == True
    assert interpreter.interpret("10 >= 5") == True
    
    print("✓ Comparison tests passed")


def test_conditionals():
    """Test if/then/else statements"""
    interpreter = SmodrInterpreter()
    
    code = """
x = 15
result = 0
IF x > 10 THEN
  result = 1
ELSE
  result = 2
END
result
"""
    assert interpreter.interpret(code) == 1
    
    print("✓ Conditional tests passed")


def test_while_loop():
    """Test while loops"""
    interpreter = SmodrInterpreter()
    
    code = """
count = 0
sum = 0
WHILE count < 5 DO
  sum = sum + count
  count = count + 1
END
sum
"""
    assert interpreter.interpret(code) == 10  # 0+1+2+3+4
    
    print("✓ While loop tests passed")


def test_functions():
    """Test function definition and calling"""
    interpreter = SmodrInterpreter()
    
    code = """
DEFINE double(x)
  RETURN x * 2
END

double(5)
"""
    assert interpreter.interpret(code) == 10
    
    print("✓ Function tests passed")


def test_recursion():
    """Test recursive functions"""
    interpreter = SmodrInterpreter()
    
    code = """
DEFINE factorial(n)
  IF n <= 1 THEN
    RETURN 1
  ELSE
    RETURN n * factorial(n - 1)
  END
END

factorial(5)
"""
    assert interpreter.interpret(code) == 120
    
    print("✓ Recursion tests passed")


def test_fibonacci():
    """Test fibonacci with recursion"""
    interpreter = SmodrInterpreter()
    
    code = """
DEFINE fib(n)
  IF n <= 1 THEN
    RETURN n
  ELSE
    RETURN fib(n - 1) + fib(n - 2)
  END
END

fib(6)
"""
    assert interpreter.interpret(code) == 8
    
    print("✓ Fibonacci tests passed")


def test_lexer():
    """Test lexer tokenization"""
    lexer = SmodrLexer("x = 10 + 5")
    tokens = lexer.tokenize()
    
    assert tokens[0].type == 'IDENTIFIER'
    assert tokens[0].value == 'x'
    assert tokens[1].type == 'ASSIGN'
    assert tokens[2].type == 'NUMBER'
    assert tokens[2].value == 10
    assert tokens[3].type == 'PLUS'
    assert tokens[4].type == 'NUMBER'
    assert tokens[4].value == 5
    
    print("✓ Lexer tests passed")


def test_parser():
    """Test parser AST generation"""
    lexer = SmodrLexer("x = 10")
    tokens = lexer.tokenize()
    parser = SmodrParser(tokens)
    ast = parser.parse()
    
    assert ast['type'] == 'PROGRAM'
    assert len(ast['statements']) == 1
    assert ast['statements'][0]['type'] == 'ASSIGN'
    assert ast['statements'][0]['name'] == 'x'
    
    print("✓ Parser tests passed")


def test_comments():
    """Test comment handling"""
    interpreter = SmodrInterpreter()
    
    code = """
# This is a comment
x = 10  # Inline comment
x
"""
    assert interpreter.interpret(code) == 10
    
    print("✓ Comment tests passed")


def test_strings():
    """Test string handling"""
    interpreter = SmodrInterpreter()
    
    code = '''
message = "Hello, World!"
message
'''
    assert interpreter.interpret(code) == "Hello, World!"
    
    print("✓ String tests passed")


def run_all_tests():
    """Run all test functions"""
    print("Running smodr test suite...\n")
    
    tests = [
        test_lexer,
        test_parser,
        test_arithmetic,
        test_variables,
        test_comparisons,
        test_conditionals,
        test_while_loop,
        test_functions,
        test_recursion,
        test_fibonacci,
        test_comments,
        test_strings,
    ]
    
    failed = 0
    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"Tests: {len(tests) - failed}/{len(tests)} passed")
    
    if failed > 0:
        print(f"Failed: {failed}")
        sys.exit(1)
    else:
        print("All tests passed! ✓")
        sys.exit(0)


if __name__ == '__main__':
    run_all_tests()
