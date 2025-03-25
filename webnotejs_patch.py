#!/usr/bin/python3

# Script to check and fix the createNote function in webnote.js
import re

# Read the current webnote.js file
with open('/var/www/webnote/webnote.js', 'r') as f:
    content = f.read()

# Look for the createNote function
create_note_match = re.search(r'createNote\s*:\s*function\s*\(.*?\{', content, re.DOTALL)
if create_note_match:
    create_note_start = create_note_match.start()
    # Find the matching closing brace
    braces = 1
    pos = create_note_match.end()
    while braces > 0 and pos < len(content):
        if content[pos] == '{':
            braces += 1
        elif content[pos] == '}':
            braces -= 1
        pos += 1
    
    function_body = content[create_note_match.start():pos]
    
    # Check if position is being handled properly
    if 'xposition' in function_body and 'yposition' in function_body:
        print("Position handling found in createNote function:")
        # Find the lines that handle xposition and yposition
        lines = function_body.split('\n')
        for i, line in enumerate(lines):
            if 'xposition' in line or 'yposition' in line:
                print(f"Line {i+1}: {line}")
    else:
        print("No position handling found in createNote function!")

# Write the findings to a log file
with open('/var/www/webnote/js_check.log', 'w') as f:
    f.write("Checking webnote.js for position handling issues\n\n")
    f.write(f"createNote function found: {'Yes' if create_note_match else 'No'}\n")
    if create_note_match:
        f.write("\nFunction body extract:\n")
        # Get a relevant excerpt
        excerpt_start = max(0, create_note_match.start() - 50)
        excerpt_end = min(len(content), pos + 50)
        f.write(content[excerpt_start:excerpt_end])
