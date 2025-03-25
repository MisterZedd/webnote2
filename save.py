#!/usr/bin/python3

import sys
import os
from xml.dom.minidom import parseString
import MySQLdb
import datetime
import traceback
import urllib.parse

try:
    # Read input data
    size = os.environ.get('CONTENT_LENGTH', 0)
    data = sys.stdin.read(int(size)).replace('\0', '')
    
    # Parse XML
    dom = parseString(data)
    wsRoot = dom.getElementsByTagName('workspace').item(0)
    
    # Get workspace name - need to unescape it
    wsname = wsRoot.getAttribute('name')
    wsname = urllib.parse.unquote(wsname)
    
    nextNoteNum = wsRoot.getAttribute('nextNoteNum')
    
    # Import database settings
    from etc.common import DBHOST, DBUSER, DBPASS, DBNAME, TABLE_PREFIX
    
    # Connect to database
    conn = MySQLdb.connect(host=DBHOST, user=DBUSER, passwd=DBPASS, db=DBNAME)
    cursor = conn.cursor()
    
    # Record current time
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Check if workspace exists
    table_name = f"{TABLE_PREFIX}workspaces0"
    cursor.execute(f"SELECT wsid FROM {table_name} WHERE wsname=%s", [wsname])
    row = cursor.fetchone()
    
    if row:
        # Update existing workspace
        wsid = row[0]
        cursor.execute(f"UPDATE {table_name} SET nextNoteNum=%s, time=%s WHERE wsid=%s", 
                      [nextNoteNum, timestamp, wsid])
    else:
        # Create new workspace
        cursor.execute(f"INSERT INTO {table_name} (wsname, nextNoteNum, time) VALUES (%s, %s, %s)",
                      [wsname, nextNoteNum, timestamp])
        wsid = cursor.lastrowid
    
    # Get notes
    nlNotes = wsRoot.getElementsByTagName('note')
    
    # Save notes
    notes_table = f"{TABLE_PREFIX}notes0"
    
    for i in range(nlNotes.length):
        note = nlNotes.item(i)
        noteid = note.getAttribute('noteid')
        bgcolor = note.getAttribute('bgcolor')
        xposition = note.getAttribute('xposition')
        yposition = note.getAttribute('yposition')
        height = note.getAttribute('height')
        width = note.getAttribute('width')
        zindex = note.getAttribute('zindex')
        
        # Get text content - use nodeValue to avoid extra encoding
        text = note.firstChild.nodeValue.strip() if note.firstChild else ""
        
        # Insert note
        cursor.execute(f"INSERT INTO {notes_table} (noteid, text, bgcolor, xposition, yposition, "
                     f"height, width, zindex, wsid, time) VALUES "
                     f"(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                     (noteid, text, bgcolor, xposition, yposition, 
                      height, width, zindex, wsid, timestamp))
    
    # Commit changes
    conn.commit()
    
    # Return success
    print('Content-type: text/xml\n')
    print('<return>\n  <status value="ok" update="%s"/>\n</return>' % timestamp)
    
except Exception as e:
    # Log error to a file
    with open('/tmp/webnote_save_error.log', 'a') as f:
        f.write(f"\n--- {datetime.datetime.now()} ---\n")
        f.write(f"Error: {str(e)}\n")
        f.write(traceback.format_exc())
        if 'data' in locals():
            f.write("\nData (first 500 chars): " + data[:500] + "\n")
    
    # Return error message
    print('Content-type: text/xml\n')
    print('<return>\n  <status value="error"/>\n</return>')
