# smodr
A self-modifying repository for a meta-language allowing for full recursive expression

## What is smodr?

smodr is an interpreted programming language designed for:
- **Self-modification**: Programs can modify their own source code during execution
- **Recursive expression**: Full support for recursive functions and meta-programming
- **Simplicity**: Clean syntax with familiar programming constructs

## Quick Start

### Installation

Clone this repository:
```bash
git clone https://github.com/lvkh1/smodr.git
cd smodr
```

### Running Programs

Execute a smodr program:
```bash
python3 smodr.py examples/hello.smodr
```

Start the interactive REPL:
```bash
python3 smodr.py
```

## Language Features

- Variables and dynamic typing
- Arithmetic and comparison operators
- Conditional statements (IF/THEN/ELSE)
- While loops
- Function definitions with recursion support
- Built-in functions (print, input, type conversions)
- Self-modifying code capabilities
- Special STOP..WORDS vocabulary for control flow

## Example

```smodr
# Calculate factorial recursively
DEFINE factorial(n)
  IF n <= 1 THEN
    RETURN 1
  ELSE
    RETURN n * factorial(n - 1)
  END
END

result = factorial(5)
print("Factorial of 5 is:", result)
```

## Documentation

For complete language specification and syntax reference, see [LANGUAGE.md](LANGUAGE.md).

## Examples

Check out the `examples/` directory for sample programs:
- `hello.smodr` - Hello World
- `arithmetic.smodr` - Basic arithmetic operations
- `conditionals.smodr` - Conditional logic
- `countdown.smodr` - While loops with STOP..WORDS
- `factorial.smodr` - Recursive factorial calculation
- `fibonacci.smodr` - Fibonacci sequence generator

## License

See [LICENSE](LICENSE) file for details.

