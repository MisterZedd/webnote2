#!/usr/bin/python3
print("Content-type: text/html\n")
print("<html><body>")
print("<h1>Debugging Information</h1>")

import sys
import os

print("<h2>Environment</h2>")
print("<pre>")
for key in sorted(os.environ.keys()):
    print(f"{key}: {os.environ[key]}")
print("</pre>")

print("<h2>Python Path</h2>")
print("<pre>")
for path in sys.path:
    print(path)
print("</pre>")

print("<h2>Python Version</h2>")
print("<pre>")
print(sys.version)
print("</pre>")

print("<h2>Installed Modules</h2>")
print("<pre>")
import pkgutil
for module in pkgutil.iter_modules():
    print(module.name)
print("</pre>")

print("</body></html>")
