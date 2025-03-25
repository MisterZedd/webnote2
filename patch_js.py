#!/usr/bin/python3

import re

# Read the webnote.js file
with open('/var/www/webnote/webnote.js', 'r') as f:
    js_content = f.read()

# Make a backup
with open('/var/www/webnote/webnote.js.bak', 'w') as f:
    f.write(js_content)

# Find the createNote function
create_note_pattern = r'(createNote\s*:\s*function\s*\(.*?\{.*?)(return.*?;)'
match = re.search(create_note_pattern, js_content, re.DOTALL)

if match:
    # Get the function content
    function_start = match.group(1)
    function_end = match.group(2)
    
    # Check if the function already has proper position handling
    if 'xposition' in function_start and '.style.left' in function_start:
        print("Note position handling already exists in createNote function")
    else:
        # Add position handling before the return statement
        position_handling = """
    // Explicit position handling added by patch
    if (options && typeof options.xposition !== 'undefined' && typeof options.yposition !== 'undefined') {
        ret.xposition = options.xposition;
        ret.yposition = options.yposition;
        ret.div.style.left = options.xposition + 'px';
        ret.div.style.top = options.yposition + 'px';
    }
    """
        # Insert the position handling before the return statement
        new_function = function_start + position_handling + function_end
        
        # Replace the function in the file
        js_content = js_content.replace(match.group(0), new_function)
        
        # Write the patched file
        with open('/var/www/webnote/webnote.js', 'w') as f:
            f.write(js_content)
        
        print("Added position handling to createNote function")
else:
    print("Could not find createNote function pattern in webnote.js")
