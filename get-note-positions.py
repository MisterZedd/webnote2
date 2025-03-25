#!/usr/bin/python3

import sys
import json
import MySQLdb
import cgi
import urllib.parse

from etc.common import *

# Print content type
print("Content-type: application/json\n")

try:
    # Get the workspace name
    form = cgi.FieldStorage()
    wsname = form.getfirst('workspace', '')
    wsname = urllib.parse.unquote(wsname)
    
    # Connect to database
    conn = MySQLdb.connect(host=DBHOST, user=DBUSER, passwd=DBPASS, db=DBNAME)
    cursor = conn.cursor()
    
    # Get workspace ID
    table_name = f"{TABLE_PREFIX}workspaces0"
    cursor.execute(f"SELECT wsid FROM {table_name} WHERE wsname=%s", [wsname])
    row = cursor.fetchone()
    
    if row:
        wsid = row[0]
        
        # Get the most recent timestamp
        notes_table = f"{TABLE_PREFIX}notes0"
        cursor.execute(f"SELECT MAX(time) FROM {notes_table} WHERE wsid=%s", [wsid])
        max_time = cursor.fetchone()[0]
        
        if max_time:
            # Get notes with positions
            cursor.execute(f"SELECT noteid, xposition, yposition FROM {notes_table} WHERE wsid=%s AND time=%s", 
                         [wsid, max_time])
            notes = cursor.fetchall()
            
            # Format as JSON
            note_data = []
            for note in notes:
                noteid, xposition, yposition = note
                note_data.append({
                    'noteid': noteid,
                    'xposition': xposition,
                    'yposition': yposition
                })
            
            # Return as JSON
            print(json.dumps(note_data))
        else:
            print("[]")
    else:
        print("[]")
    
except Exception as e:
    print(json.dumps({"error": str(e)}))
