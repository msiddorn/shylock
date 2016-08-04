for file in tests/system/test_*.py; do
    py.test "$file"
done
