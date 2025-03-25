#!/usr/bin/python3

import sys
import os
import datetime

# Log the incoming data
log_file = '/var/log/webnote_save.log'

# Get the POST data
size = os.environ.get('CONTENT_LENGTH', 0)
data = ''
if int(size) > 0:
    data = sys.stdin.read(int(size))

# Create a log entry
with open(log_file, 'a') as f:
    f.write(f"\n--- Save Request at {datetime.datetime.now()} ---\n")
    
    # Log environment variables
    f.write("Environment variables:\n")
    for key, value in os.environ.items():
        f.write(f"{key}: {value}\n")
    
    # Log POST data
    if data:
        f.write(f"\nPOST data ({size} bytes):\n{data}\n")
    
    f.write("\n")

# Now invoke the real save.py directly with the same data
# Print the XML content type
print("Content-type: text/xml\n")

try:
    # Import necessary modules
    from xml.dom.minidom import parseString
    import MySQLdb
    from etc.common import DBHOST, DBUSER, DBPASS, DBNAME, TABLE_PREFIX
    
    # Parse XML
    dom = parseString(data)
    wsRoot = dom.getElementsByTagName('workspace').item(0)
    wsname = wsRoot.getAttribute('name')
    nextNoteNum = wsRoot.getAttribute('nextNoteNum')
    
    # Log the extracted data for debugging
    with open(log_file, 'a') as f:
        f.write(f"Extracted workspace name: {wsname}\n")
        f.write(f"Extracted nextNoteNum: {nextNoteNum}\n")
    
    # Connect to database
    conn = MySQLdb.connect(host=DBHOST, user=DBUSER, passwd=DBPASS, db=DBNAME)
    cursor = conn.cursor()
    
    # Record current time
    import datetime
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
    
    # Log database operations
    with open(log_file, 'a') as f:
        f.write(f"Workspace ID: {wsid}\n")
    
    # Get notes
    nlNotes = wsRoot.getElementsByTagName('note')
    
    # Log notes count
    with open(log_file, 'a') as f:
        f.write(f"Notes count: {nlNotes.length}\n")
    
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
        
        # Get text content
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
    print('<return>\n  <status valu
# Create an updated save_log.py that properly invokes save.py
cat > /var/www/webnote/save_log.py << 'EOF'
#!/usr/bin/python3

import sys
import os
import datetime

# Log the incoming data
log_file = '/var/log/webnote_save.log'

# Get the POST data
size = os.environ.get('CONTENT_LENGTH', 0)
data = ''
if int(size) > 0:
    data = sys.stdin.read(int(size))

# Create a log entry
with open(log_file, 'a') as f:
    f.write(f"\n--- Save Request at {datetime.datetime.now()} ---\n")
    
    # Log environment variables
    f.write("Environment variables:\n")
    for key, value in os.environ.items():
        f.write(f"{key}: {value}\n")
    
    # Log POST data
    if data:
        f.write(f"\nPOST data ({size} bytes):\n{data}\n")
    
    f.write("\n")

# Now invoke the real save.py directly with the same data
# Print the XML content type
print("Content-type: text/xml\n")

try:
    # Import necessary modules
    from xml.dom.minidom import parseString
    import MySQLdb
    from etc.common import DBHOST, DBUSER, DBPASS, DBNAME, TABLE_PREFIX
    
    # Parse XML
    dom = parseString(data)
    wsRoot = dom.getElementsByTagName('workspace').item(0)
    wsname = wsRoot.getAttribute('name')
    nextNoteNum = wsRoot.getAttribute('nextNoteNum')
    
    # Log the extracted data for debugging
    with open(log_file, 'a') as f:
        f.write(f"Extracted workspace name: {wsname}\n")
        f.write(f"Extracted nextNoteNum: {nextNoteNum}\n")
    
    # Connect to database
    conn = MySQLdb.connect(host=DBHOST, user=DBUSER, passwd=DBPASS, db=DBNAME)
    cursor = conn.cursor()
    
    # Record current time
    import datetime
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
    
    # Log database operations
    with open(log_file, 'a') as f:
        f.write(f"Workspace ID: {wsid}\n")
    
    # Get notes
    nlNotes = wsRoot.getElementsByTagName('note')
    
    # Log notes count
    with open(log_file, 'a') as f:
        f.write(f"Notes count: {nlNotes.length}\n")
    
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
        
        # Get text content
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
    print('<return>\n  <status value="ok" update="%s"/>\n</return>' % timestamp)
    
    # Log success
    with open(log_file, 'a') as f:
        f.write(f"Save successful at {timestamp}\n")
    
except Exception as e:
    import traceback
    # Log error
    with open(log_file, 'a') as f:
        f.write(f"Error: {str(e)}\n")
        f.write(traceback.format_exc())
    
    # Return error message
    print('<return>\n  <status value="error"/>\n</return>')
