#!/usr/bin/python3

print("Content-type: text/html\n")
print("<html><head><title>Note Position Diagnostic</title></head><body>")
print("<h1>Note Position Diagnostic</h1>")

import sys
import MySQLdb
from etc.common import *

try:
    # Connect to the database
    conn = MySQLdb.connect(host=DBHOST, user=DBUSER, passwd=DBPASS, db=DBNAME)
    cursor = conn.cursor()
    
    # Get all workspaces
    cursor.execute(f"SELECT wsid, wsname FROM {TABLE_PREFIX}workspaces0")
    workspaces = cursor.fetchall()
    
    print("<h2>Workspaces and Notes</h2>")
    print("<table border='1'>")
    print("<tr><th>Workspace ID</th><th>Workspace Name</th><th>Note Count</th><th>Latest Time</th></tr>")
    
    for ws in workspaces:
        wsid, wsname = ws
        
        # Get latest time for this workspace
        cursor.execute(f"SELECT MAX(time) FROM {TABLE_PREFIX}notes0 WHERE wsid=%s", [wsid])
        max_time = cursor.fetchone()[0]
        
        if max_time:
            # Get notes for this workspace at the latest time
            cursor.execute(f"SELECT COUNT(*) FROM {TABLE_PREFIX}notes0 WHERE wsid=%s AND time=%s", 
                         [wsid, max_time])
            note_count = cursor.fetchone()[0]
            
            print(f"<tr><td>{wsid}</td><td>{wsname}</td><td>{note_count}</td><td>{max_time}</td></tr>")
    
    print("</table>")
    
    # Get all notes for the 'apples' workspace
    cursor.execute(f"SELECT wsid FROM {TABLE_PREFIX}workspaces0 WHERE wsname='apples'")
    apples_row = cursor.fetchone()
    
    if apples_row:
        apples_wsid = apples_row[0]
        
        # Get latest time for apples workspace
        cursor.execute(f"SELECT MAX(time) FROM {TABLE_PREFIX}notes0 WHERE wsid=%s", [apples_wsid])
        apples_max_time = cursor.fetchone()[0]
        
        if apples_max_time:
            print(f"<h2>Notes in 'apples' workspace (Latest time: {apples_max_time})</h2>")
            print("<table border='1'>")
            print("<tr><th>Note ID</th><th>Position X</th><th>Position Y</th><th>Width</th><th>Height</th><th>Text</th></tr>")
            
            # Get notes details
            cursor.execute(f"SELECT noteid, xposition, yposition, width, height, text FROM {TABLE_PREFIX}notes0 WHERE wsid=%s AND time=%s", 
                         [apples_wsid, apples_max_time])
            notes = cursor.fetchall()
            
            for note in notes:
                noteid, xpos, ypos, width, height, text = note
                print(f"<tr><td>{noteid}</td><td>{xpos}</td><td>{ypos}</td><td>{width}</td><td>{height}</td><td>{text[:50]}</td></tr>")
            
            print("</table>")
    
    print("<h2>JavaScript Implementation</h2>")
    
    # Create a simple test case to see how notes are created
    print("<div id='test-area' style='margin-top: 20px; padding: 20px; border: 1px solid #ccc;'>")
    print("<h3>Test Area</h3>")
    print("<div id='test-note' style='position: absolute; width: 150px; height: 150px; background-color: yellow; padding: 10px;'>Test Note</div>")
    print("<button onclick='moveNote()'>Move Note</button>")
    print("</div>")
    
    print("<script>")
    print("function moveNote() {")
    print("  var note = document.getElementById('test-note');")
    print("  note.style.left = '200px';")
    print("  note.style.top = '200px';")
    print("}")
    print("</script>")
    
except Exception as e:
    import traceback
    print("<h2>Error</h2>")
    print(f"<p>{str(e)}</p>")
    print("<pre>")
    print(traceback.format_exc())
    print("</pre>")

print("</body></html>")
