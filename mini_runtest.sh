#!/bin/bash

# Compile server.py if needed
# Example: python -m py_compile server.py

# Run your server.py in the background
# Example: python server.py config.txt &

# Run the tests
for test_file in tests/*.in; do
    base_name=$(basename -s .in $test_file)
    python recursor.py 1024 5 < "$test_file" | diff - "tests/${base_name}.out" > "tests/${base_name}.diff"
done
