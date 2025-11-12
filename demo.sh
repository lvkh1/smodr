#!/bin/bash
# Demo script to showcase the smodr language

echo "════════════════════════════════════════════════════════════"
echo "  smodr Language Demonstration"
echo "  A self-modifying meta-language for full recursive expression"
echo "════════════════════════════════════════════════════════════"
echo ""

echo "📝 Running Hello World..."
echo "────────────────────────────────────────────────────────────"
python3 smodr.py examples/hello.smodr
echo ""

echo "🔢 Running Arithmetic Operations..."
echo "────────────────────────────────────────────────────────────"
python3 smodr.py examples/arithmetic.smodr
echo ""

echo "⚖️  Running Conditional Logic..."
echo "────────────────────────────────────────────────────────────"
python3 smodr.py examples/conditionals.smodr
echo ""

echo "⏱️  Running Countdown with STOP..WORDS..."
echo "────────────────────────────────────────────────────────────"
python3 smodr.py examples/countdown.smodr
echo ""

echo "♻️  Running Recursive Factorial..."
echo "────────────────────────────────────────────────────────────"
python3 smodr.py examples/factorial.smodr
echo ""

echo "🔄 Running Fibonacci Sequence..."
echo "────────────────────────────────────────────────────────────"
python3 smodr.py examples/fibonacci.smodr
echo ""

echo "🔮 Running Self-Modification Example..."
echo "────────────────────────────────────────────────────────────"
python3 smodr.py examples/self_modify.smodr
echo ""

echo "════════════════════════════════════════════════════════════"
echo "✅ All demonstrations completed successfully!"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "Next steps:"
echo "  • Read LANGUAGE.md for language specification"
echo "  • Read USAGE.md for usage guide and examples"
echo "  • Try the REPL: python3 smodr.py"
echo "  • Write your own smodr programs!"
echo ""
