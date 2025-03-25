#!/usr/bin/python3

import sys
import os
from xml.dom.minidom import parseString
import MySQLdb
import datetime
import traceback
import urllib.parse

# Create log directory if it doesn't exist
os.makedirs('/tmp/webnote_logs', exist_ok=True)

# Debug function
def log_debug(msg, workspace_name=None):
    with open('/tmp/webnote_logs/save_debug.log', 'a') as f:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"[{timestamp}] ")
        if workspace_name:
            f.write(f"[{workspace_name}] ")
        f.write(f"{msg}\n")

try:
    # Read input data
    size = os.environ.get('CONTENT_LENGTH', 0)
    data = sys.stdin.read(int(size)).replace('\0', '')
    
    log_debug(f"Received data size: {len(data)}")
    log_debug(f"First 100 chars: {data[:100]}")
    
    # Parse XML
    dom = parseString(data)
    wsRoot = dom.getElementsByTagName('workspace').item(0)
    
    # Get workspace name - need to unescape it
    wsname = wsRoot.getAttribute('name')
    log_debug(f"Raw workspace name: {wsname}")
    
    wsname = urllib.parse.unquote(wsname)
    log_debug(f"Unescaped workspace name: {wsname}", wsname)
    
    nextNoteNum = wsRoot.getAttribute('nextNoteNum')
    log_debug(f"Next note number: {nextNoteNum}", wsname)
    
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
        log_debug(f"Updating existing workspace with ID {wsid}", wsname)
        cursor.execute(f"UPDATE {table_name} SET nextNoteNum=%s, time=%s WHERE wsid=%s", 
                      [nextNoteNum, timestamp, wsid])
    else:
        # Create new workspace
        log_debug(f"Creating new workspace", wsname)
        cursor.execute(f"INSERT INTO {table_name} (wsname, nextNoteNum, time) VALUES (%s, %s, %s)",
                      [wsname, nextNoteNum, timestamp])
        wsid = cursor.lastrowid
        log_debug(f"Created workspace with ID {wsid}", wsname)
    
    # Get notes
    nlNotes = wsRoot.getElementsByTagName('note')
    log_debug(f"Found {nlNotes.length} notes", wsname)
    
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
        
        log_debug(f"Note {i+1}/{nlNotes.length}: id={noteid}, pos=({xposition},{yposition}), size=({width},{height}), text={text[:30]}...", wsname)
        
        # Insert note
        cursor.execute(f"INSERT INTO {notes_table} (noteid, text, bgcolor, xposition, yposition, "
                     f"height, width, zindex, wsid, time) VALUES "
                     f"(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                     (noteid, text, bgcolor, xposition, yposition, 
                      height, width, zindex, wsid, timestamp))
    
    # Commit changes
    conn.commit()
    log_debug(f"Successfully saved workspace with {nlNotes.length} notes at {timestamp}", wsname)
    
    # Return success
    print('Content-type: text/xml\n')
    print('<return>\n  <status value="ok" update="%s"/>\n</return>' % timestamp)
    
except Exception as e:
    # Log error to a file
    with open('/tmp/webnote_logs/save_error.log', 'a') as f:
        f.write(f"\n--- {datetime.datetime.now()} ---\n")
        f.write(f"Error: {str(e)}\n")
        f.write(traceback.format_exc())
        if 'data' in locals():
            f.write("\nData (first 500 chars): " + data[:500] + "\n")
    
    log_debug(f"ERROR: {str(e)}")
    log_debug(traceback.format_exc())
    
    # Return error message
    print('Content-type: text/xml\n')
    print('<return>\n  <status value="error"/>\n</return>')
