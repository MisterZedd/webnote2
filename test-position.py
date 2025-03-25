#!/usr/bin/python3

print("Content-type: text/html\n")
print("<html><head><title>Webnote JS Analysis</title></head><body>")
print("<h1>Webnote JavaScript Analysis</h1>")

try:
    # Read the webnote.js file
    with open('/var/www/webnote/webnote.js', 'r') as f:
        js_content = f.read()
    
    # Find relevant code snippets related to positioning
    print("<h2>Code Snippets Related to Note Positioning</h2>")
    print("<pre>")
    
    lines = js_content.split("\n")
    for i, line in enumerate(lines):
        if "position" in line.lower() or "left" in line.lower() or "top" in line.lower() or "style" in line.lower():
            line_num = i + 1
            print(f"Line {line_num}: {line}")
    
    print("</pre>")
    
    # Look for the createNote function specifically
    print("<h2>createNote Function</h2>")
    print("<pre>")
    
    create_note_start = None
    create_note_end = None
    brace_count = 0
    in_function = False
    
    for i, line in enumerate(lines):
        if "createNote" in line and "{" in line:
            create_note_start = i
            in_function = True
            brace_count = line.count("{")
        
        if in_function:
            brace_count += line.count("{") - line.count("}")
            if brace_count == 0:
                create_note_end = i
                break
    
    if create_note_start is not None and create_note_end is not None:
        for i in range(create_note_start, create_note_end + 1):
            print(f"{i+1}: {lines[i]}")
    
    print("</pre>")
    
except Exception as e:
    import traceback
    print("<h2>Error</h2>")
    print(f"<p>{str(e)}</p>")
    print("<pre>")
    print(traceback.format_exc())
    print("</pre>")

print("</body></html>")
