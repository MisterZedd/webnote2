#!/usr/bin/python3

print("Content-type: text/html\n")
print("<html><body><h1>Webnote Direct Save Debug</h1>")

import sys
import os
import MySQLdb
import datetime
from xml.dom.minidom import parseString

try:
    print("<h2>Environment</h2>")
    print("<pre>")
    for key, value in os.environ.items():
        print(f"{key}: {value}")
    print("</pre>")
    
    print("<h2>Testing Database Connection</h2>")
    from etc.common import DBHOST, DBUSER, DBPASS, DBNAME, TABLE_PREFIX
    print(f"Connecting to {DBNAME} on {DBHOST} as {DBUSER}...")
    
    conn = MySQLdb.connect(host=DBHOST, user=DBUSER, passwd=DBPASS, db=DBNAME)
    cursor = conn.cursor()
    
    print("<p>Connection successful!</p>")
    
    print("<h2>Test Writing to Database</h2>")
    
    # Create test data
    wsname = "test_workspace_" + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    ws_table = f"{TABLE_PREFIX}workspaces0"
    notes_table = f"{TABLE_PREFIX}notes0"
    
    print(f"<p>Inserting test workspace '{wsname}' into {ws_table}</p>")
    
    # Insert test workspace
    cursor.execute(f"INSERT INTO {ws_table} (wsname, nextNoteNum, time) VALUES (%s, %s, %s)",
                   (wsname, 1, timestamp))
    
    wsid = cursor.lastrowid
    print(f"<p>Workspace created with ID: {wsid}</p>")
    
    # Insert test note
    print(f"<p>Inserting test note into {notes_table}</p>")
    cursor.execute(f"INSERT INTO {notes_table} (noteid, text, bgcolor, xposition, yposition, "
                   f"height, width, zindex, wsid, time) VALUES "
                   f"(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                   ("note0", "Test note", "#ffff30", 100, 100, 
                    150, 250, 1, wsid, timestamp))
    
    note_id = cursor.lastrowid
    print(f"<p>Note created with ID: {note_id}</p>")
    
    conn.commit()
    print("<p>Database operations completed successfully!</p>")
    
    print("<h2>Verify Data</h2>")
    cursor.execute(f"SELECT * FROM {ws_table} WHERE wsid=%s", [wsid])
    ws_data = cursor.fetchone()
    print("<p>Workspace data:</p>")
    print("<pre>")
    print(ws_data)
    print("</pre>")
    
    cursor.execute(f"SELECT * FROM {notes_table} WHERE wsid=%s", [wsid])
    note_data = cursor.fetchall()
    print("<p>Note data:</p>")
    print("<pre>")
    for note in note_data:
        print(note)
    print("</pre>")
    
except Exception as e:
    import traceback
    print("<h2>Error</h2>")
    print(f"<p>{str(e)}</p>")
    print("<pre>")
    traceback.print_exc(file=sys.stdout)
    print("</pre>")

print("</body></html>")
