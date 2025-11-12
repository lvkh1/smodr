# smodr Language Specification

## Overview

**smodr** is a self-modifying meta-language designed for full recursive expression. It combines imperative programming constructs with meta-programming capabilities, allowing programs to modify their own source code during execution.

## Language Features

### 1. Variables and Assignment

Variables are dynamically typed and assigned using the `=` operator:

```smodr
x = 10
name = "smodr"
pi = 3.14159
```

### 2. Arithmetic Operations

Supported operators:
- Addition: `+`
- Subtraction: `-`
- Multiplication: `*`
- Division: `/`

Example:
```smodr
result = (10 + 5) * 2 / 3
```

### 3. Comparison Operations

Supported comparison operators:
- Equal: `==`
- Not equal: `!=`
- Less than: `<`
- Greater than: `>`
- Less than or equal: `<=`
- Greater than or equal: `>=`

### 4. Conditional Statements

Use `IF`, `THEN`, `ELSE`, and `END` keywords:

```smodr
IF x > 10 THEN
  print("x is greater than 10")
ELSE
  print("x is 10 or less")
END
```

Nested conditionals are supported:
```smodr
IF score >= 90 THEN
  print("Grade: A")
ELSE
  IF score >= 80 THEN
    print("Grade: B")
  END
END
```

### 5. Loops

While loops use `WHILE`, `DO`, and `END` keywords:

```smodr
count = 0
WHILE count < 10 DO
  print(count)
  count = count + 1
END
```

### 6. Functions

Define functions using `DEFINE`, parameters in parentheses, and `END`:

```smodr
DEFINE greet(name)
  print("Hello,", name, "!")
END

greet("World")
```

Functions can return values using `RETURN`:

```smodr
DEFINE add(a, b)
  RETURN a + b
END

result = add(5, 3)
```

### 7. Recursion

Functions can call themselves recursively:

```smodr
DEFINE factorial(n)
  IF n <= 1 THEN
    RETURN 1
  ELSE
    RETURN n * factorial(n - 1)
  END
END

print(factorial(5))  # Output: 120
```

Alternatively, use the `RECURSE` keyword for explicit recursive calls:

```smodr
DEFINE fibonacci(n)
  IF n <= 1 THEN
    RETURN n
  ELSE
    RETURN RECURSE(n - 1) + RECURSE(n - 2)
  END
END
```

### 8. STOP..WORDS Vocabulary

The following keywords from `STOP..WORDS` are recognized:
- `STOP` - Can be used as a no-op or marker
- `WORDS` - Reserved
- `WAIT` - No-op
- `WATCH` - No-op
- `LISTEN` - No-op
- `PAUSE` - No-op (useful as a placeholder in loops)
- `CONTEMPLATE` - No-op
- `EAT`, `DRINK`, `SLEEP`, `REST` - No-ops
- `OBEY` - No-op

These keywords are currently implemented as no-ops but can be extended for custom control flow.

### 9. Built-in Functions

- `print(*args)` - Print values to stdout
- `input(prompt="")` - Read input from stdin
- `str(value)` - Convert to string
- `int(value)` - Convert to integer
- `float(value)` - Convert to float

### 10. Self-Modification (Advanced)

Use the `MODIFY` keyword to modify the source code during execution:

```smodr
# This is an advanced feature for meta-programming
MODIFY source "new program code here"
```

## Comments

Comments start with `#` and continue to the end of the line:

```smodr
# This is a comment
x = 5  # Inline comment
```

## Syntax Summary

```
program        → statement*

statement      → define_stmt
               | if_stmt
               | while_stmt
               | modify_stmt
               | recurse_stmt
               | return_stmt
               | expression_stmt

define_stmt    → DEFINE identifier '(' parameters? ')' block END
if_stmt        → IF expression THEN? block (ELSE block)? END
while_stmt     → WHILE expression DO? block END
modify_stmt    → MODIFY identifier expression
recurse_stmt   → RECURSE '(' arguments? ')'
return_stmt    → RETURN expression
expression_stmt → expression | identifier '=' expression

block          → '{' statement* '}' | statement*

expression     → comparison
comparison     → term (('==' | '!=' | '<' | '>' | '<=' | '>=') term)*
term           → factor (('+' | '-') factor)*
factor         → primary (('*' | '/') primary)*
primary        → NUMBER | STRING | identifier | function_call | '(' expression ')'

function_call  → identifier '(' arguments? ')'
arguments      → expression (',' expression)*
parameters     → identifier (',' identifier)*

identifier     → [a-zA-Z_][a-zA-Z0-9_]*
NUMBER         → [0-9]+ ('.' [0-9]+)?
STRING         → '"' [^"]* '"' | "'" [^']* "'"
```

## Running smodr Programs

### Execute a file:
```bash
python3 smodr.py program.smodr
```

### Interactive REPL:
```bash
python3 smodr.py
```

In REPL mode, type `exit` to quit.

## Examples

See the `examples/` directory for sample programs:
- `hello.smodr` - Hello World
- `arithmetic.smodr` - Basic arithmetic
- `conditionals.smodr` - If/else statements
- `countdown.smodr` - While loops
- `factorial.smodr` - Recursive factorial
- `fibonacci.smodr` - Fibonacci sequence
