#!/usr/bin/python3

import re

def patch_file(filename):
    # Read the file
    with open(filename, 'r') as f:
        content = f.read()
    
    # Find the createHTML method where notes are printed
    # Specifically looking for the section that prints note JavaScript
    match = re.search(r'(for n in self\.notes:.*?n\.printJavascript\(\))', content, re.DOTALL)
    
    if match:
        # Get the matched code
        original_code = match.group(1)
        
        # Create new code with position overrides
        new_code = original_code + """
    # Force correct positions for notes
    for n in self.notes:
      print("  // Override position for note " + n.noteid)
      print("  var note = workspace.notes['" + n.noteid + "'];")
      print("  if (note && note.div) {")
      print("    note.div.style.left = '" + str(n.xposition) + "px';")
      print("    note.div.style.top = '" + str(n.yposition) + "px';")
      print("    note.xposition = " + str(n.xposition) + ";")
      print("    note.yposition = " + str(n.yposition) + ";")
      print("  }")"""
        
        # Replace original code with new code
        patched_content = content.replace(original_code, new_code)
        
        # Write the patched file
        with open(filename, 'w') as f:
            f.write(patched_content)
        
        print(f"Successfully patched {filename}")
        return True
    else:
        print(f"Could not find matching pattern in {filename}")
        return False

# Patch the Workspace.py file
patch_file('/var/www/webnote/lib/Workspace.py')
