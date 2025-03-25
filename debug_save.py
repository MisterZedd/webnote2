#!/usr/bin/python3
print("Content-type: text/html\n")
print("<html><body>")
print("<h1>Debug Save Process</h1>")

import sys
import os
import traceback

try:
    print("<p>Reading input data...</p>")
    size = os.environ.get('CONTENT_LENGTH', 0)
    data = sys.stdin.read(int(size)).replace('\0', '')
    
    print(f"<p>Data size: {len(data)} characters</p>")
    print("<p>First 200 characters of data:</p>")
    print(f"<pre>{data[:200]}</pre>")
    
    print("<p>Importing modules...</p>")
    from etc.common import *
    from lib import *
    
    print("<p>Creating workspace...</p>")
    ws = Workspace.CreateSave()
    
    print(f"<p>Workspace name: {ws.name}</p>")
    print(f"<p>Next note number: {ws.nextNoteNum}</p>")
    print(f"<p>Notes count: {len(ws.notes)}</p>")
    
    for i, note in enumerate(ws.notes):
        print(f"<p>Note {i}: id={note.noteid}, text={note.text[:30]}...</p>")
    
    print("<p>Committing to database...</p>")
    updateTime = ws.commit()
    
    print(f"<p>Update time: {updateTime}</p>")
    
    print("<p>Trimming save history...</p>")
    ws.trimSaveHistory(10)
    
    print("<p>Save process completed successfully</p>")
    
    # Check if data was actually saved to the database
    print("<p>Verifying database record...</p>")
    import MySQLdb
    conn = MySQLdb.connect(host=DBHOST, user=DBUSER, passwd=DBPASS, db=DBNAME)
    cursor = conn.cursor()
    
    # Verify workspace
    cursor.execute("SELECT * FROM wn_workspaces0 WHERE wsname=%s", [ws.name])
    workspace_rows = cursor.fetchall()
    print(f"<p>Found {len(workspace_rows)} workspace records with name '{ws.name}'</p>")
    
    if workspace_rows:
        wsid = workspace_rows[0][0]
        print(f"<p>Workspace ID: {wsid}</p>")
        
        # Verify notes
        cursor.execute("SELECT * FROM wn_notes0 WHERE wsid=%s", [wsid])
        note_rows = cursor.fetchall()
        print(f"<p>Found {len(note_rows)} note records for workspace</p>")
    
except Exception as e:
    print(f"<p><strong>Error:</strong> {str(e)}</p>")
    print("<pre>")
    traceback.print_exc(file=sys.stdout)
    print("</pre>")

print("</body></html>")
