#!/usr/bin/python3
print("Content-type: text/html\n")
print("<html><body>")
print("<h1>Debug Load.py</h1>")

import sys
import traceback

try:
    print("<p>Importing modules...</p>")
    
    print("<p>Importing common...</p>")
    from etc.common import *
    print("<p>Common imported</p>")
    
    print("<p>Importing Workspace module...</p>")
    from lib.Workspace import Workspace, CreateLoad
    print("<p>Workspace module imported</p>")
    
    print("<p>Trying to create workspace...</p>")
    ws = CreateLoad()
    
    print("<p>Workspace creation result: " + str(ws) + "</p>")
    
    if ws is None:
        print("<p>Workspace is None</p>")
    else:
        print("<p>Creating HTML...</p>")
        # Don't actually call createHTML() as it outputs headers
        print("<p>Workspace name: " + ws.name + "</p>")
        print("<p>Number of notes: " + str(len(ws.notes)) + "</p>")
    
except Exception as e:
    print(f"<p><strong>Error:</strong> {str(e)}</p>")
    print("<pre>")
    traceback.print_exc(file=sys.stdout)
    print("</pre>")

print("</body></html>")
