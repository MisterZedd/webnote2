#!/usr/bin/python3

import re

# Read Workspace.py
with open('/var/www/webnote/lib/Workspace.py', 'r') as f:
    content = f.read()

# Find the section after notes are created
pattern = r'(# create notes here\s+for n in self\.notes:\s+n\.printJavascript\(\))'
match = re.search(pattern, content)

if match:
    # Add position override code after notes are created
    position_code = """\\1
    
    # Force explicit positions for notes
    for n in self.notes:
        print("  // Force position for note " + n.noteid)
        print("  if (workspace.notes['" + n.noteid + "'] && workspace.notes['" + n.noteid + "'].div) {")
        print("    workspace.notes['" + n.noteid + "'].div.style.left = '" + str(n.xposition) + "px';")
        print("    workspace.notes['" + n.noteid + "'].div.style.top = '" + str(n.yposition) + "px';")
        print("    workspace.notes['" + n.noteid + "'].xposition = " + str(n.xposition) + ";")
        print("    workspace.notes['" + n.noteid + "'].yposition = " + str(n.yposition) + ";")
        print("  }")"""
    
    modified_content = re.sub(pattern, position_code, content)
    
    # Write the modified file
    with open('/var/www/webnote/lib/Workspace.py', 'w') as f:
        f.write(modified_content)
    
    print("Successfully patched Workspace.py")
else:
    print("Could not find the pattern in Workspace.py")
