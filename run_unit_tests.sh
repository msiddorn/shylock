for file in tests/unit/test_*.py; do
    py.test "$file"
done
