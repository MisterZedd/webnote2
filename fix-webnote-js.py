#!/usr/bin/python3

import re

# Read the webnote.js file
with open('/var/www/webnote/webnote.js', 'r') as f:
    content = f.read()

# Make a backup
with open('/var/www/webnote/webnote.js.bak', 'w') as f:
    f.write(content)

# Find the createNote function
create_match = re.search(r'createNote\s*:\s*function\s*\(options\)', content)
if create_match:
    # Find where the position might be getting reset
    position_match = re.search(r'(createNote\s*:\s*function.*?)(\s*ret\.div\.style\.left\s*=.*?;)', content, re.DOTALL)
    if position_match:
        # Modify to check for provided positions first
        modified = position_match.group(1) + """
    // Check if position was specified in options
    if (options && typeof options.xposition !== 'undefined' && typeof options.yposition !== 'undefined') {
        ret.xposition = options.xposition;
        ret.yposition = options.yposition;
        ret.div.style.left = options.xposition + 'px';
        ret.div.style.top = options.yposition + 'px';
    } else {
        """ + position_match.group(2)
        
        # Replace in content
        content = content.replace(position_match.group(0), modified)
        
        # Write the modified file
        with open('/var/www/webnote/webnote.js', 'w') as f:
            f.write(content)
        
        print("Modified createNote function to respect provided positions")
    else:
        print("Could not locate position setting in createNote function")
else:
    print("Could not find createNote function")
