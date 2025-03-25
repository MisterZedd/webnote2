#!/usr/bin/python3

import re

# Read Workspace.py
with open('/var/www/webnote/lib/Workspace.py', 'r') as f:
    content = f.read()

# Backup
with open('/var/www/webnote/lib/Workspace.py.bak2', 'w') as f:
    f.write(content)

# Find the </head> tag in the HTML generation
match = re.search(r'<\/head>', content)
if match:
    # Add our position-fix.js script before </head>
    modified = content.replace('</head>', '<script type="text/javascript" src="position-fix.js"></script>\n</head>')
    
    # Write modified content
    with open('/var/www/webnote/lib/Workspace.py', 'w') as f:
        f.write(modified)
    
    print("Added position-fix.js script to Workspace.py")
else:
    print("Could not find </head> tag in Workspace.py")
