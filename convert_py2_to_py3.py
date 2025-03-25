#!/usr/bin/python3
import os
import re
import sys

def update_file(filename):
    print(f"Processing {filename}")
    with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
    
    # Fix print(statements)
    content = re.sub(r'print\s+"([^"]*)"', r'print("\1")', content)
    content = re.sub(r"print\s+'([^']*)'", r"print('\1')", content)
    content = re.sub(r'print\s+([a-zA-Z0-9_\[\]\.]+)', r'print(\1)', content)
    
    # Fix print(statements) with formatting
    content = re.sub(r'print\s+(.*?),\s*(.*)', r'print(\1, \2)', content)
    
    # Fix exceptions
    content = re.sub(r'except\s+([a-zA-Z0-9_]+),\s+([a-zA-Z0-9_]+):', r'except \1 as \2:', content)
    
    # Replace xrange with range
    content = re.sub(r'xrange\(', r'range(', content)
    
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)
    
    print(f"Updated {filename}")

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                update_file(os.path.join(root, file))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if os.path.isfile(path):
            update_file(path)
        elif os.path.isdir(path):
            process_directory(path)
    else:
        process_directory('/var/www/webnote')
