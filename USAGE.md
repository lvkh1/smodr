# smodr Usage Guide

## Getting Started

### Prerequisites

- Python 3.6 or higher

### Running smodr Programs

#### Execute a File

```bash
python3 smodr.py path/to/program.smodr
```

Example:
```bash
python3 smodr.py examples/hello.smodr
```

#### Interactive REPL

Start the Read-Eval-Print Loop (REPL):

```bash
python3 smodr.py
```

In the REPL, you can:
- Type expressions and see results immediately
- Define variables and functions
- Test code snippets
- Type `exit` to quit

Example REPL session:
```
smodr v0.1.0 - Self-modifying meta-language
Type 'exit' to quit

smodr> 5 + 3
8
smodr> x = 10
10
smodr> x * 2
20
smodr> DEFINE double(n)
...   RETURN n * 2
... END
smodr> double(7)
14
smodr> exit
```

## Writing Your First Program

### Hello World

Create a file `hello.smodr`:

```smodr
# My first smodr program
print("Hello, World!")
```

Run it:
```bash
python3 smodr.py hello.smodr
```

### Variables and Arithmetic

```smodr
# Variables don't need declaration
x = 10
y = 20

# Arithmetic operations
sum = x + y
difference = x - y
product = x * y
quotient = y / x

print("Sum:", sum)
print("Difference:", difference)
print("Product:", product)
print("Quotient:", quotient)
```

### Conditionals

```smodr
age = 25

IF age >= 18 THEN
  print("You are an adult")
ELSE
  print("You are a minor")
END
```

### Loops

```smodr
# Count from 1 to 10
i = 1
WHILE i <= 10 DO
  print(i)
  i = i + 1
END
```

### Functions

```smodr
# Define a function to calculate the square
DEFINE square(n)
  RETURN n * n
END

# Use the function
result = square(7)
print("7 squared is", result)
```

### Recursion

```smodr
# Calculate factorial recursively
DEFINE factorial(n)
  IF n <= 1 THEN
    RETURN 1
  ELSE
    RETURN n * factorial(n - 1)
  END
END

print("5! =", factorial(5))
```

## Advanced Features

### Nested Functions

Functions can call other functions:

```smodr
DEFINE is_even(n)
  remainder = n - (n / 2) * 2
  IF remainder == 0 THEN
    RETURN 1
  ELSE
    RETURN 0
  END
END

DEFINE print_even_odd(n)
  IF is_even(n) THEN
    print(n, "is even")
  ELSE
    print(n, "is odd")
  END
END

print_even_odd(7)
print_even_odd(8)
```

### Multiple Parameters

Functions can take multiple parameters:

```smodr
DEFINE add_three(a, b, c)
  RETURN a + b + c
END

total = add_three(10, 20, 30)
print("Total:", total)
```

### Using STOP..WORDS

The STOP..WORDS vocabulary can be used for control flow markers:

```smodr
count = 5

WHILE count > 0 DO
  print("Countdown:", count)
  PAUSE  # Marker for potential pause point
  count = count - 1
END

print("STOP")  # End marker
```

## Tips and Best Practices

### 1. Use Meaningful Variable Names

```smodr
# Good
total_price = quantity * unit_price

# Less clear
x = a * b
```

### 2. Add Comments

```smodr
# Calculate the area of a circle
radius = 5
pi = 3.14159
area = pi * radius * radius  # A = πr²
```

### 3. Keep Functions Focused

```smodr
# Good: Each function does one thing
DEFINE celsius_to_fahrenheit(c)
  RETURN c * 9 / 5 + 32
END

DEFINE fahrenheit_to_celsius(f)
  RETURN (f - 32) * 5 / 9
END
```

### 4. Use Recursion Carefully

Recursion is powerful but can be slow for large inputs. Consider iterative solutions for performance-critical code.

```smodr
# Recursive (simple but slower for large n)
DEFINE fib_recursive(n)
  IF n <= 1 THEN
    RETURN n
  ELSE
    RETURN fib_recursive(n - 1) + fib_recursive(n - 2)
  END
END

# Iterative (faster)
DEFINE fib_iterative(n)
  IF n <= 1 THEN
    RETURN n
  END
  
  a = 0
  b = 1
  i = 2
  
  WHILE i <= n DO
    temp = a + b
    a = b
    b = temp
    i = i + 1
  END
  
  RETURN b
END
```

### 5. Test Your Code

Use the REPL to test small pieces of code before putting them in a file.

## Common Patterns

### Input and Output

```smodr
# Get user input
name = input("What is your name? ")
print("Hello,", name, "!")

# Note: input() is a built-in function
```

### Type Conversions

```smodr
# Convert string to number
age_str = "25"
age = int(age_str)

# Convert number to string
count = 42
count_str = str(count)

# Convert to float
price = float("19.99")
```

### Accumulation Pattern

```smodr
# Sum numbers from 1 to 100
sum = 0
i = 1
WHILE i <= 100 DO
  sum = sum + i
  i = i + 1
END
print("Sum:", sum)
```

### Finding Maximum

```smodr
DEFINE max(a, b)
  IF a > b THEN
    RETURN a
  ELSE
    RETURN b
  END
END

result = max(15, 23)
print("Maximum:", result)
```

## Troubleshooting

### Common Errors

**Syntax Error: Unexpected token**
- Check for missing END keywords
- Verify parentheses are balanced
- Ensure quotes match

**Undefined variable**
- Make sure variable is assigned before use
- Check for typos in variable names

**Undefined function**
- Define functions before calling them
- Verify function name spelling

### Getting Help

- Read the [Language Specification](LANGUAGE.md)
- Check the examples in the `examples/` directory
- Experiment in the REPL

## Next Steps

1. Try all the examples in the `examples/` directory
2. Write your own programs
3. Explore the language specification for advanced features
4. Experiment with self-modification capabilities (advanced)

Happy coding with smodr!
